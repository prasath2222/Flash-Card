import { useState, useRef, useEffect, useMemo } from 'react';
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Menu,
  Pencil,
  Plus,
  RotateCw,
  Settings,
  Sparkles,
  Volume2,
  X,
  Zap,
  BookOpen,
  Layers,
  Check,
  BookmarkCheck,
  Shuffle,
  VolumeX,
} from 'lucide-react';
import { INITIAL_CARDS, Flashcard } from './cardsData';

type View = 'home' | 'subsections' | 'flashcard';

interface SubDeck {
  id: string;
  title: string;
  count: string;
  progress: string;
  category: string;
  active?: boolean;
}

interface Deck {
  id: string;
  title: string;
  desc: string;
  subDecks: SubDeck[];
}

const DEFAULT_DECKS: Deck[] = [
  {
    id: '3k',
    title: '3K Vocabulary',
    desc: 'Core Vocabulary Deck',
    subDecks: [
      {
        id: '800-1000',
        title: 'Cards 800 – 1000',
        count: '199 cards',
        progress: '85%',
        category: 'Kitchen, Tools & Daily Living',
        active: true,
      },
      {
        id: '600-800',
        title: 'Cards 600 – 800',
        count: '200 cards',
        progress: '100%',
        category: 'Nature, Weather & Science',
      },
      {
        id: '400-600',
        title: 'Cards 400 – 600',
        count: '200 cards',
        progress: '100%',
        category: 'Society, Careers & City',
      },
    ],
  },
];

export default function App() {
  // Primary view management: 'home', 'subsections', 'flashcard'
  const [view, setView] = useState<View>('home');

  // Decks list state
  const [decks, setDecks] = useState<Deck[]>(DEFAULT_DECKS);

  // Active sub-deck tracking
  const [activeSubDeckId, setActiveSubDeckId] = useState<string>('800-1000');

  // Drawer / Settings sidebar state
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Flashcards state
  const [cards, setCards] = useState<Flashcard[]>(() => {
    try {
      const saved = localStorage.getItem('vocab_custom_cards');
      if (saved) return JSON.parse(saved);
    } catch {
      // ignore
    }
    return INITIAL_CARDS;
  });

  // Current flashcard index & flip state
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  // Audio & speech settings
  const [speechVolume, setSpeechVolume] = useState(1);
  const [speechRate, setSpeechRate] = useState(0.85);
  const [speechPitch, setSpeechPitch] = useState(1);
  const [soundFxVolume, setSoundFxVolume] = useState(1);

  // Learned cards set
  const [learnedCards, setLearnedCards] = useState<Set<number>>(() => {
    try {
      const saved = localStorage.getItem('vocab_react_learned');
      if (saved) return new Set(JSON.parse(saved));
    } catch {
      // ignore
    }
    return new Set();
  });

  // Edit card modal state
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editFormData, setEditFormData] = useState<{
    word: string;
    tamil: string;
    spanish: string;
    hindi: string;
    category: string;
  }>({ word: '', tamil: '', spanish: '', hindi: '', category: '' });

  // Memory shortcut modal state
  const [isShortcutModalOpen, setIsShortcutModalOpen] = useState(false);
  const [shortcutFormData, setShortcutFormData] = useState<{
    shortcutEs: string;
    shortcutHi: string;
  }>({ shortcutEs: '', shortcutHi: '' });

  // Toast notifications
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const toastTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const showToast = (msg: string) => {
    if (toastTimeoutRef.current) clearTimeout(toastTimeoutRef.current);
    setToastMessage(msg);
    toastTimeoutRef.current = setTimeout(() => {
      setToastMessage(null);
    }, 2200);
  };

  const currentCard = cards[currentIndex] || cards[0];
  const isCurrentLearned = learnedCards.has(currentCard?.num);

  // Sound effect oscillator
  const playFlipSound = () => {
    if (soundFxVolume <= 0.05) return;
    try {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(isFlipped ? 520 : 660, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(isFlipped ? 220 : 280, ctx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.35 * soundFxVolume, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.14);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.15);
    } catch {
      // AudioContext unavailable or blocked
    }
  };

  // High-fidelity speech synthesizer using server endpoint or Web Speech API
  const speakWord = async (text: string, lang: 'en' | 'es' | 'hi' = 'en') => {
    if (!text) return;
    const clean = text.split('/')[0].trim();

    // Try server TTS audio proxy first for native accent quality
    try {
      const audio = new Audio(`/api/tts?text=${encodeURIComponent(clean)}&lang=${lang}`);
      audio.volume = speechVolume;
      await audio.play();
      return;
    } catch {
      // Fallback to browser SpeechSynthesis
    }

    try {
      window.speechSynthesis?.cancel();
      const utter = new SpeechSynthesisUtterance(clean);
      utter.volume = speechVolume;
      utter.rate = speechRate;
      utter.pitch = speechPitch;
      utter.lang = lang === 'es' ? 'es-ES' : lang === 'hi' ? 'hi-IN' : 'en-US';
      window.speechSynthesis?.speak(utter);
    } catch {
      // Speech synthesis unsupported
    }
  };

  // Flip action
  const handleFlip = () => {
    playFlipSound();
    setIsFlipped((prev) => !prev);
  };

  // Double-tap or click detection on card
  const lastTapRef = useRef<number>(0);
  const handleCardTap = (e: React.MouseEvent | React.TouchEvent) => {
    const target = e.target as HTMLElement;
    if (target.closest('button, input, textarea, .no-flip, .action-btn')) {
      return;
    }
    const now = Date.now();
    const diff = now - lastTapRef.current;
    if (diff > 40 && diff < 450) {
      lastTapRef.current = 0;
      handleFlip();
    } else {
      lastTapRef.current = now;
    }
  };

  // Previous & Next navigation
  const handlePrev = () => {
    if (currentIndex > 0) {
      setIsFlipped(false);
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < cards.length - 1) {
      setIsFlipped(false);
      setCurrentIndex((prev) => prev + 1);
    }
  };

  // Shuffle deck
  const handleShuffle = () => {
    const shuffled = [...cards];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    setCards(shuffled);
    setCurrentIndex(0);
    setIsFlipped(false);
    showToast('Deck shuffled!');
  };

  // Toggle card learned state
  const toggleLearned = (cardNum: number) => {
    setLearnedCards((prev) => {
      const next = new Set(prev);
      if (next.has(cardNum)) {
        next.delete(cardNum);
        showToast(`Card #${cardNum} moved to review`);
      } else {
        next.add(cardNum);
        showToast(`✓ Card #${cardNum} marked as Learned!`);
      }
      try {
        localStorage.setItem('vocab_react_learned', JSON.stringify([...next]));
      } catch {
        // ignore
      }
      return next;
    });
  };

  // Open edit modal
  const openEditModal = () => {
    setEditFormData({
      word: currentCard.word,
      tamil: currentCard.tamil,
      spanish: currentCard.spanish,
      hindi: currentCard.hindi,
      category: currentCard.category,
    });
    setIsEditModalOpen(true);
  };

  // Save edit form
  const handleSaveEdit = (e: React.FormEvent) => {
    e.preventDefault();
    const updated = cards.map((c, idx) =>
      idx === currentIndex
        ? {
            ...c,
            word: editFormData.word.trim().toUpperCase() || c.word,
            tamil: editFormData.tamil.trim() || c.tamil,
            spanish: editFormData.spanish.trim() || c.spanish,
            hindi: editFormData.hindi.trim() || c.hindi,
            category: editFormData.category.trim() || c.category,
          }
        : c
    );
    setCards(updated);
    try {
      localStorage.setItem('vocab_custom_cards', JSON.stringify(updated));
    } catch {
      // ignore
    }
    setIsEditModalOpen(false);
    showToast(`Translations for #${currentCard.num} saved!`);
  };

  // Save shortcut form
  const handleSaveShortcut = (e: React.FormEvent) => {
    e.preventDefault();
    const updated = cards.map((c, idx) =>
      idx === currentIndex
        ? {
            ...c,
            shortcutEs: shortcutFormData.shortcutEs.trim() || c.shortcutEs,
            shortcutHi: shortcutFormData.shortcutHi.trim() || c.shortcutHi,
          }
        : c
    );
    setCards(updated);
    try {
      localStorage.setItem('vocab_custom_cards', JSON.stringify(updated));
    } catch {
      // ignore
    }
    setIsShortcutModalOpen(false);
    showToast(`Memory Shortcuts for #${currentCard.num} saved!`);
  };

  // Reset learned progress
  const handleResetLearned = () => {
    setLearnedCards(new Set());
    try {
      localStorage.removeItem('vocab_react_learned');
    } catch {
      // ignore
    }
    showToast('Learned cards progress reset');
  };

  // Calculate overall stats
  const activeDeck = decks.find((d) => d.id === '3k') || decks[0];
  const learnedRatio = useMemo(() => {
    return Math.round((learnedCards.size / cards.length) * 100);
  }, [learnedCards.size, cards.length]);

  return (
    <div className="relative flex flex-col w-full h-[100dvh] max-w-[500px] mx-auto bg-[#0B0B0E] text-white overflow-hidden antialiased select-none font-sans">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-5 left-1/2 -translate-x-1/2 z-[10000] px-4 py-2 rounded-full bg-[#181822]/95 border border-[#38bdf8]/40 shadow-xl shadow-black/70 text-sm font-semibold text-white flex items-center gap-2 animate-fade-in pointer-events-none">
          <Sparkles className="w-4 h-4 text-[#38bdf8]" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Edit Translations Modal */}
      {isEditModalOpen && (
        <div
          className="fixed inset-0 z-[10000] bg-black/75 backdrop-blur-xs flex items-center justify-center p-4"
          onClick={() => setIsEditModalOpen(false)}
        >
          <div
            className="w-full max-w-sm bg-[#16161F] border border-white/12 rounded-2xl p-5 shadow-2xl space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-white/8 pb-3">
              <h3 className="text-base font-bold text-white">
                Edit Translations (#{currentCard.num})
              </h3>
              <button
                type="button"
                onClick={() => setIsEditModalOpen(false)}
                className="text-[#8A8A93] hover:text-white cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleSaveEdit} className="space-y-3 text-xs font-semibold">
              <div>
                <label className="text-[#8A8A93] block mb-1">English Word</label>
                <input
                  type="text"
                  value={editFormData.word}
                  onChange={(e) => setEditFormData({ ...editFormData, word: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0B0E] border border-white/10 text-white font-bold uppercase focus:border-[#2563EB] outline-none"
                />
              </div>
              <div>
                <label className="text-[#8A8A93] block mb-1">Native Tamil Script</label>
                <input
                  type="text"
                  value={editFormData.tamil}
                  onChange={(e) => setEditFormData({ ...editFormData, tamil: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0B0E] border border-white/10 text-emerald-400 font-bold focus:border-[#2563EB] outline-none tamil-font text-base"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[#8A8A93] block mb-1">Spanish (Español)</label>
                  <input
                    type="text"
                    value={editFormData.spanish}
                    onChange={(e) => setEditFormData({ ...editFormData, spanish: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg bg-[#0B0B0E] border border-white/10 text-white focus:border-[#2563EB] outline-none"
                  />
                </div>
                <div>
                  <label className="text-[#8A8A93] block mb-1">Hindi</label>
                  <input
                    type="text"
                    value={editFormData.hindi}
                    onChange={(e) => setEditFormData({ ...editFormData, hindi: e.target.value })}
                    className="w-full px-3 py-2 rounded-lg bg-[#0B0B0E] border border-white/10 text-white focus:border-[#2563EB] outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="text-[#8A8A93] block mb-1">Category</label>
                <input
                  type="text"
                  value={editFormData.category}
                  onChange={(e) => setEditFormData({ ...editFormData, category: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0B0E] border border-white/10 text-white focus:border-[#2563EB] outline-none"
                />
              </div>
              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsEditModalOpen(false)}
                  className="flex-1 py-2 rounded-lg bg-white/5 border border-white/10 text-[#8A8A93] hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 rounded-lg bg-[#2563EB] hover:bg-[#1d4ed8] text-white font-bold cursor-pointer"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Memory Shortcut Modal */}
      {isShortcutModalOpen && (
        <div
          className="fixed inset-0 z-[10000] bg-black/75 backdrop-blur-xs flex items-center justify-center p-4"
          onClick={() => setIsShortcutModalOpen(false)}
        >
          <div
            className="w-full max-w-sm bg-[#16161F] border border-white/12 rounded-2xl p-5 shadow-2xl space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-white/8 pb-3">
              <h3 className="text-base font-bold text-white flex items-center gap-1.5">
                <Zap className="w-4 h-4 text-amber-400" />
                <span>Memory Punchlines (#{currentCard.num})</span>
              </h3>
              <button
                type="button"
                onClick={() => setIsShortcutModalOpen(false)}
                className="text-[#8A8A93] hover:text-white cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleSaveShortcut} className="space-y-3 text-xs font-semibold">
              <div>
                <label className="text-rose-400 block mb-1 font-bold">Spanish Memory Trick</label>
                <textarea
                  rows={3}
                  value={shortcutFormData.shortcutEs}
                  onChange={(e) =>
                    setShortcutFormData({ ...shortcutFormData, shortcutEs: e.target.value })
                  }
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0B0E] border border-white/10 text-white focus:border-[#2563EB] outline-none resize-none leading-relaxed"
                />
              </div>
              <div>
                <label className="text-amber-400 block mb-1 font-bold">Hindi Memory Trick</label>
                <textarea
                  rows={3}
                  value={shortcutFormData.shortcutHi}
                  onChange={(e) =>
                    setShortcutFormData({ ...shortcutFormData, shortcutHi: e.target.value })
                  }
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0B0E] border border-white/10 text-white focus:border-[#2563EB] outline-none resize-none leading-relaxed"
                />
              </div>
              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsShortcutModalOpen(false)}
                  className="flex-1 py-2 rounded-lg bg-white/5 border border-white/10 text-[#8A8A93] hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 rounded-lg bg-[#2563EB] hover:bg-[#1d4ed8] text-white font-bold cursor-pointer"
                >
                  Save Tricks
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Menu / Settings Drawer */}
      {isMenuOpen && (
        <div
          className="fixed inset-0 z-[9999] bg-black/70 backdrop-blur-xs flex transition-opacity"
          onClick={() => setIsMenuOpen(false)}
        >
          <aside
            className="w-[85%] max-w-[320px] h-full bg-[#121217] border-r border-white/8 flex flex-col shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between p-5 border-b border-white/8">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Settings className="w-5 h-5 text-[#38bdf8]" />
                <span>Deck Settings</span>
              </h2>
              <button
                type="button"
                className="p-1 rounded-lg text-[#8A8A93] hover:text-white cursor-pointer"
                onClick={() => setIsMenuOpen(false)}
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-5 space-y-5">
              <div className="space-y-4 text-xs font-semibold text-[#8A8A93]">
                <div>
                  <div className="flex justify-between mb-1">
                    <span>Speech Volume</span>
                    <span className="text-white">{Math.round(speechVolume * 100)}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={Math.round(speechVolume * 100)}
                    onChange={(e) => setSpeechVolume(Number(e.target.value) / 100)}
                    className="w-full h-1.5 bg-[#26262E] rounded-full appearance-none accent-[#2563EB] cursor-pointer"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span>Voice Speed (Rate)</span>
                    <span className="text-white">{speechRate.toFixed(2)}x</span>
                  </div>
                  <input
                    type="range"
                    min="50"
                    max="150"
                    value={Math.round(speechRate * 100)}
                    onChange={(e) => setSpeechRate(Number(e.target.value) / 100)}
                    className="w-full h-1.5 bg-[#26262E] rounded-full appearance-none accent-[#2563EB] cursor-pointer"
                  />
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span>Card Sound FX</span>
                    <span className="text-white">{Math.round(soundFxVolume * 100)}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={Math.round(soundFxVolume * 100)}
                    onChange={(e) => setSoundFxVolume(Number(e.target.value) / 100)}
                    className="w-full h-1.5 bg-[#26262E] rounded-full appearance-none accent-[#2563EB] cursor-pointer"
                  />
                </div>
              </div>

              <div className="pt-4 border-t border-white/8 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-[#8A8A93]">Learned Cards</span>
                  <span className="font-bold text-emerald-400">
                    {learnedCards.size} / {cards.length} ({learnedRatio}%)
                  </span>
                </div>
                <button
                  type="button"
                  onClick={handleResetLearned}
                  className="w-full py-2 px-3 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 text-xs font-semibold text-[#8A8A93] hover:text-white transition-colors cursor-pointer text-center"
                >
                  Reset Learned Progress
                </button>
              </div>

              <div className="pt-4 border-t border-white/8">
                <div className="p-3 rounded-xl bg-white/4 border border-white/6 text-xs text-[#8A8A93] space-y-1">
                  <p className="font-bold text-white">4 Languages Mode</p>
                  <p>English · Spanish · Hindi · Pure Native Tamil</p>
                </div>
              </div>
            </div>
          </aside>
        </div>
      )}

      {/* VIEW 1: HOME VIEW ('home') */}
      {view === 'home' && (
        <div className="flex flex-col flex-1 h-full overflow-hidden">
          {/* Top Header */}
          <header className="flex items-center justify-between px-5 py-4 border-b border-white/8 bg-[#0B0B0E] shrink-0">
            <button
              type="button"
              className="p-1.5 -ml-1.5 rounded-lg text-white hover:bg-white/8 transition-colors cursor-pointer"
              onClick={() => setIsMenuOpen(true)}
              aria-label="Open menu"
            >
              <Menu className="w-5 h-5 text-white" />
            </button>
            <h1 className="text-[18px] font-bold text-white tracking-tight">Decks</h1>
            <div className="w-5 h-5" />
          </header>

          {/* Home Content - Displays the '3K Vocabulary' card */}
          <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3.5">
            {decks.map((deck) => (
              <div
                key={deck.id}
                role="button"
                tabIndex={0}
                onClick={() => setView('subsections')}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    setView('subsections');
                  }
                }}
                className="w-full bg-[#16161E] border border-white/8 rounded-2xl p-5 hover:border-[#2563EB]/50 hover:bg-[#1a1a24] transition-all duration-200 cursor-pointer text-left group shadow-lg"
              >
                <div className="flex items-center justify-between">
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-xl bg-blue-500/15 border border-blue-500/30 flex items-center justify-center text-blue-400">
                        <BookOpen className="w-4 h-4" />
                      </div>
                      <h2 className="text-xl font-bold text-white tracking-tight">{deck.title}</h2>
                    </div>
                    <p className="text-xs font-medium text-[#8A8A93] pl-10">
                      {deck.subDecks.length} Decks Available · {deck.desc}
                    </p>
                  </div>
                  <ChevronRight className="w-5 h-5 text-[#8A8A93] group-hover:text-white transition-colors group-hover:translate-x-0.5 duration-150" />
                </div>

                <div className="mt-4 pt-3 border-t border-white/6 flex items-center justify-between text-xs text-[#8A8A93]">
                  <span className="flex items-center gap-1.5 text-blue-400 font-semibold">
                    <Layers className="w-3.5 h-3.5" />
                    Multilingual Decks
                  </span>
                  <span>{deck.subDecks[0]?.count || '199 cards'}</span>
                </div>
              </div>
            ))}

            {/* Add Section Button */}
            <button
              type="button"
              onClick={() => showToast('New vocabulary section added')}
              className="w-full py-3.5 px-4 rounded-full bg-transparent border border-dashed border-white/15 text-[#EDEDED] text-sm font-medium flex items-center justify-center gap-2 hover:border-[#2563EB] hover:text-white hover:bg-[#2563EB]/8 transition-all cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Add Section</span>
            </button>
          </div>
        </div>
      )}

      {/* VIEW 2: SUBSECTIONS VIEW ('subsections') */}
      {view === 'subsections' && (
        <div className="flex flex-col flex-1 h-full overflow-hidden">
          {/* Header */}
          <header className="flex items-center justify-between px-5 py-4 border-b border-white/8 bg-[#0B0B0E] shrink-0">
            <button
              type="button"
              className="flex items-center gap-1.5 text-sm font-semibold text-[#8A8A93] hover:text-white transition-colors cursor-pointer"
              onClick={() => setView('home')}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Decks</span>
            </button>
            <h1 className="text-[18px] font-bold text-white tracking-tight">3K Vocabulary</h1>
            <button
              type="button"
              onClick={() => showToast('Editing sections list')}
              className="text-xs font-semibold px-2.5 py-1 rounded-md border border-white/10 text-[#8A8A93] hover:text-white cursor-pointer"
            >
              Edit
            </button>
          </header>

          {/* Subsections List */}
          <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3.5">
            {activeDeck.subDecks.map((subDeck) => {
              const isActive = subDeck.id === '800-1000' || subDeck.active;
              return (
                <div
                  key={subDeck.id}
                  role="button"
                  tabIndex={0}
                  onClick={() => {
                    setActiveSubDeckId(subDeck.id);
                    if (isActive) {
                      setView('flashcard');
                    } else {
                      showToast(`${subDeck.title} loaded`);
                    }
                  }}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      setView('flashcard');
                    }
                  }}
                  className={`w-full bg-[#16161E] border rounded-2xl p-5 transition-all duration-200 cursor-pointer text-left group shadow-lg ${
                    isActive
                      ? 'border-[#2563EB]/60 hover:border-[#2563EB] bg-[#171926]'
                      : 'border-white/8 hover:border-white/20'
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <h3 className="text-base font-bold text-white tracking-tight">
                        {subDeck.title}
                      </h3>
                      {isActive && (
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#2563EB] text-white">
                          Active
                        </span>
                      )}
                    </div>
                    <ChevronRight className="w-4 h-4 text-[#8A8A93] group-hover:text-white transition-colors" />
                  </div>

                  <div className="w-full h-1.5 bg-[#26262E] rounded-full overflow-hidden mb-2.5">
                    <div
                      className={`h-full rounded-full transition-all ${
                        isActive ? 'bg-[#2563EB]' : 'bg-[#14B8A6]'
                      }`}
                      style={{ width: subDeck.progress }}
                    />
                  </div>

                  <div className="flex items-center justify-between text-xs text-[#8A8A93]">
                    <span>{subDeck.category || 'General Vocabulary'}</span>
                    <span className="font-semibold text-white/90">{subDeck.count}</span>
                  </div>
                </div>
              );
            })}

            {/* Add Sub-section Button */}
            <button
              type="button"
              onClick={() => showToast('Sub-section added')}
              className="w-full py-3.5 px-4 rounded-full bg-transparent border border-dashed border-white/15 text-[#EDEDED] text-sm font-medium flex items-center justify-center gap-2 hover:border-[#2563EB] hover:text-white hover:bg-[#2563EB]/8 transition-all cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Add Sub-section</span>
            </button>
          </div>
        </div>
      )}

      {/* VIEW 3: FLASHCARD VIEW ('flashcard') */}
      {view === 'flashcard' && (
        <div className="flex flex-col flex-1 h-full overflow-hidden">
          {/* Header */}
          <header className="flex items-center justify-between px-5 py-4 border-b border-white/8 bg-[#0B0B0E] shrink-0">
            <button
              type="button"
              className="flex items-center gap-1.5 text-sm font-semibold text-[#8A8A93] hover:text-white transition-colors cursor-pointer"
              onClick={() => setView('subsections')}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Cards 800 – 1000</span>
            </button>
            <div className="text-sm font-bold tabular-nums text-[#8A8A93]">
              <strong className="text-white">#{currentCard?.num || 800}</strong>
              <span className="text-[#8A8A93]/70"> / 1000</span>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                className="p-1.5 rounded-lg text-[#8A8A93] hover:text-white transition-colors cursor-pointer"
                onClick={handleShuffle}
                title="Shuffle deck"
              >
                <Shuffle className="w-4 h-4" />
              </button>
              <button
                type="button"
                className="p-1.5 rounded-lg text-[#8A8A93] hover:text-white transition-colors cursor-pointer"
                onClick={() => setIsMenuOpen(true)}
                aria-label="Settings"
              >
                <Settings className="w-4 h-4" />
              </button>
            </div>
          </header>

          {/* Slim progress bar */}
          <div className="w-full h-1 bg-white/6 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#38bdf8] via-[#818cf8] to-[#10b981] transition-all duration-300"
              style={{
                width: `${Math.round(((currentIndex + 1) / cards.length) * 100)}%`,
              }}
            />
          </div>

          {/* Flashcard Stage */}
          <div className="flex-1 flex flex-col justify-center items-center px-4 py-3 overflow-y-auto">
            <div
              onClick={handleCardTap}
              className="w-full max-w-[420px] min-h-[460px] bg-[#121624] border border-white/10 rounded-3xl p-5 flex flex-col justify-between shadow-2xl relative select-none hover:border-white/20 transition-all duration-200 cursor-pointer"
            >
              {/* Back Face */}
              {isFlipped ? (
                <div className="flex-1 flex flex-col justify-between space-y-3">
                  <div className="flex items-center justify-between shrink-0">
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-white/6 border border-white/10 text-[#8A8A93]">
                      #{currentCard.num}
                    </span>
                    <span className="px-3 py-0.5 rounded-full bg-[#0e2238] border border-[#38bdf8]/40 text-[#38bdf8] text-xs font-bold uppercase tracking-wide">
                      {currentCard.word}
                    </span>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        openEditModal();
                      }}
                      className="p-1.5 rounded-lg bg-white/6 hover:bg-white/12 text-[#8A8A93] hover:text-white border border-white/10 transition-colors cursor-pointer no-flip"
                      title="Edit Translations"
                    >
                      <Pencil className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {/* Native Tamil Display */}
                  <div className="w-full bg-[#0c1f2d]/85 border border-[#14b8a6]/45 rounded-2xl py-5 px-4 shadow-[0_0_24px_rgba(20,184,166,0.18)] flex items-center justify-center text-center">
                    <h2 className="tamil-font text-3xl sm:text-4xl font-extrabold text-white tracking-wide">
                      {currentCard.tamil || '—'}
                    </h2>
                  </div>

                  {/* Multilingual Grid: Spanish & Hindi */}
                  <div className="grid grid-cols-2 gap-2.5">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        speakWord(currentCard.spanish, 'es');
                      }}
                      className="p-3 rounded-2xl bg-[#191d2d] border border-white/8 hover:border-white/18 text-left transition-all cursor-pointer group/tile no-flip"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-950/70 border border-rose-500/35 text-rose-300 uppercase tracking-wider">
                          ES ESPAÑOL
                        </span>
                        <Volume2 className="w-3.5 h-3.5 text-[#8A8A93] group-hover/tile:text-white" />
                      </div>
                      <p className="text-base font-bold text-white tracking-tight">
                        {currentCard.spanish || '—'}
                      </p>
                    </button>

                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        speakWord(currentCard.hindi, 'hi');
                      }}
                      className="p-3 rounded-2xl bg-[#191d2d] border border-white/8 hover:border-white/18 text-left transition-all cursor-pointer group/tile no-flip"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-950/70 border border-amber-500/35 text-amber-300 uppercase tracking-wider">
                          HI हिन्दी
                        </span>
                        <Volume2 className="w-3.5 h-3.5 text-[#8A8A93] group-hover/tile:text-white" />
                      </div>
                      <p className="text-base font-bold text-white tracking-tight">
                        {currentCard.hindi || '—'}
                      </p>
                    </button>
                  </div>

                  {/* Memory Shortcut Box */}
                  <div
                    onClick={(e) => {
                      e.stopPropagation();
                      setShortcutFormData({
                        shortcutEs: currentCard.shortcutEs || '',
                        shortcutHi: currentCard.shortcutHi || '',
                      });
                      setIsShortcutModalOpen(true);
                    }}
                    className="p-3 rounded-xl bg-amber-500/8 border border-amber-500/25 cursor-pointer hover:bg-amber-500/12 transition-all no-flip"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1">
                        <Zap className="w-3 h-3 text-amber-400" />
                        Memory Trick
                      </span>
                      <Pencil className="w-3 h-3 text-amber-400/80" />
                    </div>
                    <p className="text-xs text-amber-100/90 line-clamp-2 leading-relaxed">
                      {currentCard.shortcutEs || currentCard.shortcutHi || 'Tap to add a mnemonic punchline!'}
                    </p>
                  </div>

                  <div className="flex items-center justify-center text-[11px] text-[#8A8A93] gap-1 pt-1">
                    <span>Double-tap to flip back</span>
                  </div>
                </div>
              ) : (
                /* Front Face */
                <div className="flex-1 flex flex-col justify-between space-y-3">
                  <div className="flex items-center justify-between shrink-0">
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-white/6 border border-white/10 text-[#8A8A93]">
                      #{currentCard.num}
                    </span>
                    <span className="text-xs font-semibold px-3 py-1 rounded-full bg-white/6 border border-white/10 text-[#8A8A93] truncate max-w-[170px]">
                      {currentCard.category}
                    </span>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        speakWord(currentCard.word, 'en');
                      }}
                      className="p-2 rounded-xl bg-white/6 hover:bg-white/12 text-white border border-white/10 transition-colors cursor-pointer no-flip"
                      title="Listen English pronunciation"
                    >
                      <Volume2 className="w-4 h-4 text-[#38bdf8]" />
                    </button>
                  </div>

                  {/* HD Photograph or Emoji Fallback */}
                  <div className="relative w-full h-44 sm:h-48 rounded-2xl overflow-hidden bg-black/40 border border-white/8 flex items-center justify-center shadow-inner group/img">
                    {currentCard.imageUrl ? (
                      <img
                        src={currentCard.imageUrl}
                        alt={currentCard.word}
                        className="w-full h-full object-cover transition-transform duration-300 group-hover/img:scale-105"
                        loading="lazy"
                        onError={(e) => {
                          // Hide broken image
                          (e.target as HTMLElement).style.display = 'none';
                        }}
                      />
                    ) : (
                      <span className="text-5xl">{currentCard.emoji || '✨'}</span>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-[#0B0B0E]/80 via-transparent to-transparent pointer-events-none" />
                  </div>

                  {/* Target English Word */}
                  <div className="text-center py-1">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-[#38bdf8] block mb-1">
                      English
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
                      {currentCard.word}
                    </h2>
                  </div>

                  <div className="flex items-center justify-center text-[11px] text-[#8A8A93] gap-1 pt-1">
                    <span>Double-tap to flip card ↺</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Bottom Navigation Bar */}
          <footer className="px-5 py-4 border-t border-white/8 bg-[#0B0B0E] shrink-0 space-y-2">
            <div className="flex items-center justify-between gap-3">
              <button
                type="button"
                onClick={handlePrev}
                disabled={currentIndex === 0}
                className="flex-1 py-3 px-4 rounded-xl bg-[#16161E] border border-white/8 text-sm font-bold text-white hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-1.5 transition-all cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Prev</span>
              </button>

              <button
                type="button"
                onClick={handleFlip}
                className="py-3 px-5 rounded-xl bg-[#2563EB]/15 border border-[#2563EB]/40 text-sm font-bold text-[#38bdf8] hover:bg-[#2563EB]/30 flex items-center justify-center gap-1.5 transition-all cursor-pointer shadow-lg shadow-[#2563EB]/10"
              >
                <RotateCw className="w-4 h-4" />
                <span>Flip</span>
              </button>

              <button
                type="button"
                onClick={handleNext}
                disabled={currentIndex === cards.length - 1}
                className="flex-1 py-3 px-4 rounded-xl bg-[#16161E] border border-white/8 text-sm font-bold text-white hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-1.5 transition-all cursor-pointer"
              >
                <span>Next</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>

            <div className="flex items-center justify-between pt-1">
              <button
                type="button"
                onClick={() => toggleLearned(currentCard.num)}
                className={`w-full py-2 px-3 rounded-lg text-xs font-bold flex items-center justify-center gap-1.5 transition-all cursor-pointer ${
                  isCurrentLearned
                    ? 'bg-emerald-950/60 border border-emerald-500/40 text-emerald-300'
                    : 'bg-white/4 border border-white/8 text-[#8A8A93] hover:text-white'
                }`}
              >
                <BookmarkCheck className="w-3.5 h-3.5" />
                <span>{isCurrentLearned ? '✓ Learned Card' : 'Mark as Learned'}</span>
              </button>
            </div>
          </footer>
        </div>
      )}
    </div>
  );
}
