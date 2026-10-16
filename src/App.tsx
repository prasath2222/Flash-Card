import { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
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
  VolumeX,
  X,
  Zap,
  BookOpen,
  Layers,
  Check,
  BookmarkCheck,
  Bookmark,
  Trash2,
  Undo2,
  Shuffle,
  Sliders,
  Play,
  RotateCcw,
  Sparkle,
  SlidersHorizontal,
  Flame,
  Award,
} from 'lucide-react';
import { INITIAL_CARDS, Flashcard } from './cardsData';

type View = 'home' | 'subsections' | 'flashcard';
type SettingsTab = 'audio' | 'study' | 'deck';

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
    desc: 'Core Multilingual Master Deck',
    subDecks: [
      {
        id: '800-1000',
        title: 'Cards 800 – 1000',
        count: '199 cards',
        progress: '100%',
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
  // Primary view navigation
  const [view, setView] = useState<View>('flashcard');

  // Decks list state
  const [decks] = useState<Deck[]>(DEFAULT_DECKS);
  const [activeSubDeckId, setActiveSubDeckId] = useState<string>('800-1000');

  // Settings drawer & tab
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [settingsTab, setSettingsTab] = useState<SettingsTab>('audio');

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

  // Deleted cards pool for restoring
  const [deletedCards, setDeletedCards] = useState<Flashcard[]>(() => {
    try {
      const saved = localStorage.getItem('vocab_deleted_cards');
      if (saved) return JSON.parse(saved);
    } catch {
      // ignore
    }
    return [];
  });

  // Navigation index & direction for framer-motion slide
  const [currentIndex, setCurrentIndex] = useState(0);
  const [direction, setDirection] = useState<number>(1);
  const [isFlipped, setIsFlipped] = useState(false);

  // Audio & Speech Settings
  const [speechVolume, setSpeechVolume] = useState<number>(() => {
    const v = localStorage.getItem('vocab_speech_vol');
    return v !== null ? Number(v) : 1;
  });
  const [speechRate, setSpeechRate] = useState<number>(() => {
    const v = localStorage.getItem('vocab_speech_rate');
    return v !== null ? Number(v) : 0.9;
  });
  const [speechPitch, setSpeechPitch] = useState<number>(1);
  const [soundFxVolume, setSoundFxVolume] = useState<number>(() => {
    const v = localStorage.getItem('vocab_sfx_vol');
    return v !== null ? Number(v) : 0.8;
  });
  const [soundProfile, setSoundProfile] = useState<'whoosh' | 'snap' | 'pop'>('whoosh');

  // Study Settings
  const [autoAdvance, setAutoAdvance] = useState<boolean>(() => {
    return localStorage.getItem('vocab_auto_advance') === 'true';
  });

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

  const showToast = useCallback((msg: string) => {
    if (toastTimeoutRef.current) clearTimeout(toastTimeoutRef.current);
    setToastMessage(msg);
    toastTimeoutRef.current = setTimeout(() => {
      setToastMessage(null);
    }, 2200);
  }, []);

  // Persist settings
  useEffect(() => {
    localStorage.setItem('vocab_speech_vol', String(speechVolume));
    localStorage.setItem('vocab_speech_rate', String(speechRate));
    localStorage.setItem('vocab_sfx_vol', String(soundFxVolume));
    localStorage.setItem('vocab_auto_advance', String(autoAdvance));
  }, [speechVolume, speechRate, soundFxVolume, autoAdvance]);

  // Current Card helper
  const currentCard = useMemo(() => {
    if (!cards.length) return INITIAL_CARDS[0];
    const safeIdx = Math.min(Math.max(currentIndex, 0), cards.length - 1);
    return cards[safeIdx] || cards[0];
  }, [cards, currentIndex]);

  const isCurrentLearned = learnedCards.has(currentCard?.num);

  // Sound FX Audio Synthesizer
  const playSoundEffect = useCallback(
    (type: 'slide' | 'flip' | 'learned' | 'delete') => {
      if (soundFxVolume <= 0.05) return;
      try {
        const AudioCtx =
          window.AudioContext ||
          (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        if (type === 'slide') {
          // Dynamic slide whoosh
          osc.type = 'sine';
          osc.frequency.setValueAtTime(soundProfile === 'snap' ? 680 : 340, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(
            soundProfile === 'snap' ? 120 : 180,
            ctx.currentTime + 0.12
          );
          gain.gain.setValueAtTime(0.25 * soundFxVolume, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.13);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.14);
        } else if (type === 'flip') {
          // Flip sound
          osc.type = soundProfile === 'pop' ? 'triangle' : 'sine';
          const startFreq = isFlipped ? 540 : 640;
          const endFreq = isFlipped ? 260 : 320;
          osc.frequency.setValueAtTime(startFreq, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(endFreq, ctx.currentTime + 0.11);
          gain.gain.setValueAtTime(0.3 * soundFxVolume, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.13);
        } else if (type === 'learned') {
          // Two-tone cheerful chime
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
          osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.08); // E5
          gain.gain.setValueAtTime(0.35 * soundFxVolume, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.22);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.24);
        } else if (type === 'delete') {
          // Low drop sound
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(300, ctx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(80, ctx.currentTime + 0.15);
          gain.gain.setValueAtTime(0.2 * soundFxVolume, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.16);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.17);
        }
      } catch {
        // AudioContext blocked or unavailable
      }
    },
    [soundFxVolume, soundProfile, isFlipped]
  );

  // High-fidelity speech synthesizer using server endpoint or Web Speech API
  const speakWord = useCallback(
    async (text: string, lang: 'en' | 'es' | 'hi' | 'ta' = 'en') => {
      if (!text) return;
      const clean = text.split('/')[0].trim();

      // Try server TTS audio proxy first for native accent quality
      try {
        const audio = new Audio(
          `/api/tts?text=${encodeURIComponent(clean)}&lang=${encodeURIComponent(lang)}`
        );
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
        utter.lang =
          lang === 'es' ? 'es-ES' : lang === 'hi' ? 'hi-IN' : lang === 'ta' ? 'ta-IN' : 'en-US';
        window.speechSynthesis?.speak(utter);
      } catch {
        // Speech synthesis unsupported
      }
    },
    [speechVolume, speechRate, speechPitch]
  );

  // Flip card
  const handleFlip = useCallback(() => {
    playSoundEffect('flip');
    setIsFlipped((prev) => !prev);
  }, [playSoundEffect]);

  // Navigate Next with Framer Motion slide effect
  const handleNext = useCallback(() => {
    if (currentIndex < cards.length - 1) {
      playSoundEffect('slide');
      setDirection(1);
      setIsFlipped(false);
      setCurrentIndex((prev) => prev + 1);
    }
  }, [currentIndex, cards.length, playSoundEffect]);

  // Navigate Prev with Framer Motion slide effect
  const handlePrev = useCallback(() => {
    if (currentIndex > 0) {
      playSoundEffect('slide');
      setDirection(-1);
      setIsFlipped(false);
      setCurrentIndex((prev) => prev - 1);
    }
  }, [currentIndex, playSoundEffect]);

  // Jump to specific card
  const handleJumpToCard = (targetIdx: number) => {
    if (targetIdx < 0 || targetIdx >= cards.length || targetIdx === currentIndex) return;
    playSoundEffect('slide');
    setDirection(targetIdx > currentIndex ? 1 : -1);
    setIsFlipped(false);
    setCurrentIndex(targetIdx);
  };

  // Keyboard Navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (isEditModalOpen || isShortcutModalOpen || isMenuOpen) return;
      if (view !== 'flashcard') return;

      if (e.key === 'ArrowRight' || e.key === 'j') {
        e.preventDefault();
        handleNext();
      } else if (e.key === 'ArrowLeft' || e.key === 'k') {
        e.preventDefault();
        handlePrev();
      } else if (e.key === ' ' || e.key === 'Enter' || e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        e.preventDefault();
        handleFlip();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isEditModalOpen, isShortcutModalOpen, isMenuOpen, view, handleNext, handlePrev, handleFlip]);

  // Double-tap or card tap detection
  const lastTapRef = useRef<number>(0);
  const handleCardTap = (e: React.MouseEvent | React.TouchEvent) => {
    const target = e.target as HTMLElement;
    if (target.closest('button, input, textarea, a, .no-flip, .action-btn')) {
      return;
    }
    const now = Date.now();
    const diff = now - lastTapRef.current;
    if (diff > 40 && diff < 380) {
      lastTapRef.current = 0;
      handleFlip();
    } else {
      lastTapRef.current = now;
    }
  };

  // Toggle card learned state
  const toggleLearned = (cardNum: number) => {
    setLearnedCards((prev) => {
      const next = new Set(prev);
      const isNowLearned = !next.has(cardNum);
      if (isNowLearned) {
        next.add(cardNum);
        playSoundEffect('learned');
        showToast(`✓ #${cardNum} Marked as Learned!`);
        if (autoAdvance && currentIndex < cards.length - 1) {
          setTimeout(() => handleNext(), 300);
        }
      } else {
        next.delete(cardNum);
        showToast(`Card #${cardNum} returned to Review`);
      }
      try {
        localStorage.setItem('vocab_react_learned', JSON.stringify([...next]));
      } catch {
        // ignore
      }
      return next;
    });
  };

  // Delete current card with restore option
  const handleDeleteCurrentCard = () => {
    if (cards.length <= 1) {
      showToast('Cannot delete the last remaining card');
      return;
    }
    const cardToDelete = cards[currentIndex];
    const newCards = cards.filter((_, idx) => idx !== currentIndex);
    const newDeleted = [cardToDelete, ...deletedCards];

    setCards(newCards);
    setDeletedCards(newDeleted);
    playSoundEffect('delete');

    try {
      localStorage.setItem('vocab_custom_cards', JSON.stringify(newCards));
      localStorage.setItem('vocab_deleted_cards', JSON.stringify(newDeleted));
    } catch {
      // ignore
    }

    if (currentIndex >= newCards.length) {
      setCurrentIndex(Math.max(0, newCards.length - 1));
    }
    setIsFlipped(false);
    showToast(`Deleted #${cardToDelete.num} (can be restored in Settings)`);
  };

  // Restore all deleted cards
  const handleRestoreDeletedCards = () => {
    if (!deletedCards.length) {
      showToast('No deleted cards to restore');
      return;
    }
    const restored = [...cards, ...deletedCards].sort((a, b) => a.num - b.num);
    setCards(restored);
    setDeletedCards([]);
    try {
      localStorage.setItem('vocab_custom_cards', JSON.stringify(restored));
      localStorage.removeItem('vocab_deleted_cards');
    } catch {
      // ignore
    }
    showToast(`Restored ${deletedCards.length} deleted cards!`);
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
    showToast('⚡ Deck Shuffled!');
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

  // Reset entire deck to default 199 cards
  const handleResetToDefaultDeck = () => {
    setCards(INITIAL_CARDS);
    setDeletedCards([]);
    setCurrentIndex(0);
    setIsFlipped(false);
    setLearnedCards(new Set());
    try {
      localStorage.removeItem('vocab_custom_cards');
      localStorage.removeItem('vocab_deleted_cards');
      localStorage.removeItem('vocab_react_learned');
    } catch {
      // ignore
    }
    showToast('Deck reset to factory defaults (199 cards)');
  };

  // Stats calculation
  const activeDeck = decks.find((d) => d.id === '3k') || decks[0];
  const learnedCount = learnedCards.size;
  const learnedRatio = Math.round((learnedCount / (cards.length || 1)) * 100);

  // Framer Motion Slide Variants for card transitions
  const slideVariants = {
    enter: (dir: number) => ({
      x: dir > 0 ? 280 : -280,
      opacity: 0,
      scale: 0.94,
      rotate: dir > 0 ? 3 : -3,
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1,
      scale: 1,
      rotate: 0,
      transition: {
        x: { type: 'spring' as const, stiffness: 340, damping: 28 },
        opacity: { duration: 0.2 },
        scale: { duration: 0.2 },
        rotate: { duration: 0.2 },
      },
    },
    exit: (dir: number) => ({
      zIndex: 0,
      x: dir < 0 ? 280 : -280,
      opacity: 0,
      scale: 0.94,
      rotate: dir < 0 ? 3 : -3,
      transition: {
        x: { type: 'spring' as const, stiffness: 340, damping: 28 },
        opacity: { duration: 0.18 },
        scale: { duration: 0.18 },
        rotate: { duration: 0.18 },
      },
    }),
  };

  return (
    <div className="relative flex flex-col w-full h-[100dvh] max-w-[540px] mx-auto bg-[#070a13] text-[#f8fafc] overflow-hidden antialiased select-none font-sans shadow-2xl">
      {/* Toast Notification */}
      <AnimatePresence>
        {toastMessage && (
          <motion.div
            initial={{ opacity: 0, y: -20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -16, scale: 0.9 }}
            transition={{ duration: 0.18 }}
            className="fixed top-5 left-1/2 -translate-x-1/2 z-[10000] px-4 py-2.5 rounded-2xl bg-[#0f172a]/95 border border-[#38bdf8]/40 shadow-2xl shadow-black/80 text-xs font-bold text-white flex items-center gap-2 pointer-events-none backdrop-blur-md"
          >
            <Sparkles className="w-4 h-4 text-[#38bdf8] shrink-0 animate-pulse" />
            <span>{toastMessage}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Edit Translations Modal */}
      {isEditModalOpen && (
        <div
          className="fixed inset-0 z-[10000] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-150"
          onClick={() => setIsEditModalOpen(false)}
        >
          <div
            className="w-full max-w-sm bg-[#0f172a] border border-white/15 rounded-3xl p-5 shadow-2xl space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <div className="flex items-center gap-2">
                <Pencil className="w-4 h-4 text-[#38bdf8]" />
                <h3 className="text-base font-bold text-white">
                  Edit Card #{currentCard.num}
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setIsEditModalOpen(false)}
                className="p-1 rounded-xl text-[#94a3b8] hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleSaveEdit} className="space-y-3 text-xs font-semibold">
              <div>
                <label className="text-[#94a3b8] block mb-1">English Word</label>
                <input
                  type="text"
                  value={editFormData.word}
                  onChange={(e) => setEditFormData({ ...editFormData, word: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[#070a13] border border-white/12 text-white font-bold uppercase focus:border-[#38bdf8] outline-none"
                />
              </div>
              <div>
                <label className="text-[#94a3b8] block mb-1">Native Tamil Script</label>
                <input
                  type="text"
                  value={editFormData.tamil}
                  onChange={(e) => setEditFormData({ ...editFormData, tamil: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[#070a13] border border-white/12 text-emerald-400 font-bold focus:border-[#38bdf8] outline-none tamil-font text-base"
                />
              </div>
              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="text-[#94a3b8] block mb-1">Spanish (Español)</label>
                  <input
                    type="text"
                    value={editFormData.spanish}
                    onChange={(e) => setEditFormData({ ...editFormData, spanish: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-[#070a13] border border-white/12 text-white focus:border-[#38bdf8] outline-none"
                  />
                </div>
                <div>
                  <label className="text-[#94a3b8] block mb-1">Hindi (हिन्दी)</label>
                  <input
                    type="text"
                    value={editFormData.hindi}
                    onChange={(e) => setEditFormData({ ...editFormData, hindi: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-[#070a13] border border-white/12 text-white focus:border-[#38bdf8] outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="text-[#94a3b8] block mb-1">Category</label>
                <input
                  type="text"
                  value={editFormData.category}
                  onChange={(e) => setEditFormData({ ...editFormData, category: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl bg-[#070a13] border border-white/12 text-white focus:border-[#38bdf8] outline-none"
                />
              </div>
              <div className="flex gap-2.5 pt-2">
                <button
                  type="button"
                  onClick={() => setIsEditModalOpen(false)}
                  className="flex-1 py-2.5 rounded-xl bg-white/6 border border-white/10 text-[#94a3b8] hover:text-white cursor-pointer font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-[#0284c7] to-[#0ea5e9] hover:from-[#0369a1] hover:to-[#0284c7] text-white font-bold cursor-pointer shadow-lg shadow-sky-900/30"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Memory Shortcut Modal */}
      {isShortcutModalOpen && (
        <div
          className="fixed inset-0 z-[10000] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-150"
          onClick={() => setIsShortcutModalOpen(false)}
        >
          <div
            className="w-full max-w-sm bg-[#0f172a] border border-white/15 rounded-3xl p-5 shadow-2xl space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <div className="flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                <h3 className="text-base font-bold text-white">
                  Memory Trick (#{currentCard.num})
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setIsShortcutModalOpen(false)}
                className="p-1 rounded-xl text-[#94a3b8] hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleSaveShortcut} className="space-y-3 text-xs font-semibold">
              <div>
                <label className="text-rose-400 block mb-1 font-bold">Spanish Mnemonic</label>
                <textarea
                  rows={3}
                  value={shortcutFormData.shortcutEs}
                  onChange={(e) =>
                    setShortcutFormData({ ...shortcutFormData, shortcutEs: e.target.value })
                  }
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[#070a13] border border-white/12 text-white focus:border-rose-400 outline-none resize-none leading-relaxed"
                  placeholder="e.g. Sounds like... reminds of..."
                />
              </div>
              <div>
                <label className="text-amber-400 block mb-1 font-bold">Hindi Mnemonic</label>
                <textarea
                  rows={3}
                  value={shortcutFormData.shortcutHi}
                  onChange={(e) =>
                    setShortcutFormData({ ...shortcutFormData, shortcutHi: e.target.value })
                  }
                  className="w-full px-3.5 py-2.5 rounded-xl bg-[#070a13] border border-white/12 text-white focus:border-amber-400 outline-none resize-none leading-relaxed"
                  placeholder="e.g. Rhymes with... connects to..."
                />
              </div>
              <div className="flex gap-2.5 pt-2">
                <button
                  type="button"
                  onClick={() => setIsShortcutModalOpen(false)}
                  className="flex-1 py-2.5 rounded-xl bg-white/6 border border-white/10 text-[#94a3b8] hover:text-white cursor-pointer font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-black font-bold cursor-pointer shadow-lg shadow-amber-900/30"
                >
                  Save Tricks
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Redesigned World-Class Settings Section Modal */}
      <AnimatePresence>
        {isMenuOpen && (
          <div
            className="fixed inset-0 z-[9999] bg-black/75 backdrop-blur-md flex items-end sm:items-center justify-center p-0 sm:p-4"
            onClick={() => setIsMenuOpen(false)}
          >
            <motion.div
              initial={{ y: '100%', opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: '100%', opacity: 0 }}
              transition={{ type: 'spring', damping: 28, stiffness: 300 }}
              className="w-full max-w-md max-h-[90vh] bg-[#0c1222] border border-white/15 rounded-t-[32px] sm:rounded-[32px] flex flex-col shadow-2xl overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Settings Header */}
              <div className="flex items-center justify-between px-6 pt-5 pb-4 border-b border-white/10">
                <div className="flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-[#38bdf8]/20 to-[#818cf8]/20 border border-[#38bdf8]/40 flex items-center justify-center text-[#38bdf8] shadow-inner">
                    <SlidersHorizontal className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="text-base font-extrabold text-white tracking-tight">
                      Preferences & Settings
                    </h2>
                    <p className="text-[11px] font-medium text-[#94a3b8]">
                      Customise audio, gestures & deck data
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setIsMenuOpen(false)}
                  className="p-2 rounded-2xl bg-white/6 hover:bg-white/12 text-[#94a3b8] hover:text-white transition-colors cursor-pointer border border-white/8"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Segmented Pill Navigation */}
              <div className="px-6 pt-3.5 pb-2">
                <div className="grid grid-cols-3 gap-1 p-1 bg-[#141d33] rounded-2xl border border-white/10">
                  <button
                    type="button"
                    onClick={() => setSettingsTab('audio')}
                    className={`py-2 px-2 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
                      settingsTab === 'audio'
                        ? 'bg-[#38bdf8] text-[#070a13] shadow-md shadow-[#38bdf8]/20'
                        : 'text-[#94a3b8] hover:text-white'
                    }`}
                  >
                    <Volume2 className="w-3.5 h-3.5" />
                    <span>Audio</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setSettingsTab('study')}
                    className={`py-2 px-2 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
                      settingsTab === 'study'
                        ? 'bg-[#38bdf8] text-[#070a13] shadow-md shadow-[#38bdf8]/20'
                        : 'text-[#94a3b8] hover:text-white'
                    }`}
                  >
                    <Zap className="w-3.5 h-3.5" />
                    <span>Study</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setSettingsTab('deck')}
                    className={`py-2 px-2 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
                      settingsTab === 'deck'
                        ? 'bg-[#38bdf8] text-[#070a13] shadow-md shadow-[#38bdf8]/20'
                        : 'text-[#94a3b8] hover:text-white'
                    }`}
                  >
                    <Layers className="w-3.5 h-3.5" />
                    <span>Deck Data</span>
                  </button>
                </div>
              </div>

              {/* Settings Body */}
              <div className="flex-1 overflow-y-auto px-6 py-3 space-y-4 text-xs font-semibold">
                {settingsTab === 'audio' && (
                  <div className="space-y-4">
                    {/* Speech Volume Slider */}
                    <div className="p-4 rounded-2xl bg-[#141e34]/70 border border-white/8 space-y-2.5">
                      <div className="flex items-center justify-between">
                        <span className="text-white flex items-center gap-1.5 font-bold">
                          <Volume2 className="w-4 h-4 text-[#38bdf8]" />
                          Speech Volume
                        </span>
                        <span className="px-2 py-0.5 rounded-lg bg-sky-950/80 border border-sky-500/30 text-sky-300 font-mono text-[11px]">
                          {Math.round(speechVolume * 100)}%
                        </span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={Math.round(speechVolume * 100)}
                        onChange={(e) => setSpeechVolume(Number(e.target.value) / 100)}
                        className="w-full h-1.5 bg-[#1e293b] rounded-full appearance-none accent-[#38bdf8] cursor-pointer"
                      />
                    </div>

                    {/* Speech Speed Presets & Slider */}
                    <div className="p-4 rounded-2xl bg-[#141e34]/70 border border-white/8 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-white font-bold flex items-center gap-1.5">
                          <Sliders className="w-4 h-4 text-[#38bdf8]" />
                          Voice Speed (Rate)
                        </span>
                        <span className="px-2 py-0.5 rounded-lg bg-sky-950/80 border border-sky-500/30 text-sky-300 font-mono text-[11px]">
                          {speechRate.toFixed(2)}x
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-2">
                        {[0.75, 0.9, 1.15].map((rate) => (
                          <button
                            key={rate}
                            type="button"
                            onClick={() => setSpeechRate(rate)}
                            className={`py-1.5 rounded-xl border text-[11px] font-bold transition-all cursor-pointer ${
                              Math.abs(speechRate - rate) < 0.05
                                ? 'bg-sky-500/20 border-[#38bdf8] text-[#38bdf8]'
                                : 'bg-[#0f172a] border-white/10 text-[#94a3b8] hover:text-white'
                            }`}
                          >
                            {rate === 0.75 ? '0.75x Slow' : rate === 0.9 ? '0.90x Clean' : '1.15x Fast'}
                          </button>
                        ))}
                      </div>
                      <input
                        type="range"
                        min="50"
                        max="140"
                        value={Math.round(speechRate * 100)}
                        onChange={(e) => setSpeechRate(Number(e.target.value) / 100)}
                        className="w-full h-1.5 bg-[#1e293b] rounded-full appearance-none accent-[#38bdf8] cursor-pointer"
                      />
                    </div>

                    {/* Card Sound FX */}
                    <div className="p-4 rounded-2xl bg-[#141e34]/70 border border-white/8 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-white font-bold flex items-center gap-1.5">
                          <RotateCw className="w-4 h-4 text-emerald-400" />
                          Card Sound FX & Haptics
                        </span>
                        <span className="px-2 py-0.5 rounded-lg bg-emerald-950/80 border border-emerald-500/30 text-emerald-300 font-mono text-[11px]">
                          {Math.round(soundFxVolume * 100)}%
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-2">
                        {(['whoosh', 'snap', 'pop'] as const).map((prof) => (
                          <button
                            key={prof}
                            type="button"
                            onClick={() => {
                              setSoundProfile(prof);
                              playSoundEffect('slide');
                            }}
                            className={`py-1.5 rounded-xl border text-[11px] capitalize font-bold transition-all cursor-pointer ${
                              soundProfile === prof
                                ? 'bg-emerald-500/20 border-emerald-400 text-emerald-300'
                                : 'bg-[#0f172a] border-white/10 text-[#94a3b8] hover:text-white'
                            }`}
                          >
                            {prof}
                          </button>
                        ))}
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={Math.round(soundFxVolume * 100)}
                        onChange={(e) => setSoundFxVolume(Number(e.target.value) / 100)}
                        className="w-full h-1.5 bg-[#1e293b] rounded-full appearance-none accent-emerald-400 cursor-pointer"
                      />
                    </div>

                    {/* Test Audio Output Button */}
                    <button
                      type="button"
                      onClick={() => speakWord(currentCard.word, 'en')}
                      className="w-full py-2.5 px-4 rounded-xl bg-white/6 hover:bg-white/10 border border-white/10 text-white font-bold flex items-center justify-center gap-2 transition-all cursor-pointer"
                    >
                      <Play className="w-3.5 h-3.5 text-[#38bdf8]" />
                      <span>Test English Voice: "{currentCard.word}"</span>
                    </button>
                  </div>
                )}

                {settingsTab === 'study' && (
                  <div className="space-y-4">
                    {/* Auto-Advance Toggle */}
                    <div className="p-4 rounded-2xl bg-[#141e34]/70 border border-white/8 flex items-center justify-between">
                      <div className="space-y-0.5">
                        <span className="text-white font-bold block">Auto-Advance on Learned</span>
                        <p className="text-[11px] text-[#94a3b8]">
                          Automatically slide to next card when marked learned
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setAutoAdvance(!autoAdvance)}
                        className={`w-12 h-6 rounded-full transition-colors p-0.5 relative cursor-pointer ${
                          autoAdvance ? 'bg-emerald-500' : 'bg-[#1e293b]'
                        }`}
                      >
                        <div
                          className={`w-5 h-5 rounded-full bg-white shadow-md transition-transform ${
                            autoAdvance ? 'translate-x-6' : 'translate-x-0'
                          }`}
                        />
                      </button>
                    </div>

                    {/* Gestures Guide */}
                    <div className="p-4 rounded-2xl bg-[#141e34]/70 border border-white/8 space-y-2.5">
                      <span className="text-white font-bold block">Touch & Keyboard Gestures</span>
                      <ul className="space-y-1.5 text-[11px] text-[#94a3b8]">
                        <li className="flex items-center justify-between">
                          <span>Swipe Left / Right</span>
                          <span className="text-white font-mono bg-white/6 px-1.5 py-0.5 rounded">
                            Next / Prev Card
                          </span>
                        </li>
                        <li className="flex items-center justify-between">
                          <span>Double-Tap Card</span>
                          <span className="text-white font-mono bg-white/6 px-1.5 py-0.5 rounded">
                            Flip Front / Back
                          </span>
                        </li>
                        <li className="flex items-center justify-between">
                          <span>Keyboard [← / →]</span>
                          <span className="text-white font-mono bg-white/6 px-1.5 py-0.5 rounded">
                            Navigate
                          </span>
                        </li>
                        <li className="flex items-center justify-between">
                          <span>Keyboard [Space]</span>
                          <span className="text-white font-mono bg-white/6 px-1.5 py-0.5 rounded">
                            Flip Card
                          </span>
                        </li>
                      </ul>
                    </div>

                    {/* Multilingual Mode Info */}
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-950/40 to-slate-900/60 border border-indigo-500/20 text-[#94a3b8] space-y-1">
                      <p className="font-bold text-white flex items-center gap-1.5">
                        <Award className="w-4 h-4 text-indigo-400" />
                        4-Language Integration
                      </p>
                      <p className="text-[11px]">
                        English · Español · हिन्दी · Authentic Tamil (தூய தமிழ் எழுத்து)
                      </p>
                    </div>
                  </div>
                )}

                {settingsTab === 'deck' && (
                  <div className="space-y-4">
                    {/* Mastery Stats Bar */}
                    <div className="p-4 rounded-2xl bg-[#141e34]/70 border border-white/8 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-white font-bold">Vocabulary Mastery</span>
                        <span className="text-emerald-400 font-mono font-bold text-sm">
                          {learnedRatio}%
                        </span>
                      </div>
                      <div className="w-full h-2.5 bg-[#1e293b] rounded-full overflow-hidden p-0.5 border border-white/5">
                        <div
                          className="h-full bg-gradient-to-r from-sky-400 via-indigo-400 to-emerald-400 rounded-full transition-all duration-300"
                          style={{ width: `${learnedRatio}%` }}
                        />
                      </div>
                      <div className="grid grid-cols-3 gap-2 text-center pt-1">
                        <div className="p-2 rounded-xl bg-[#0f172a] border border-white/6">
                          <span className="block text-[10px] text-[#94a3b8] uppercase">Learned</span>
                          <span className="text-sm font-extrabold text-emerald-400">
                            {learnedCount}
                          </span>
                        </div>
                        <div className="p-2 rounded-xl bg-[#0f172a] border border-white/6">
                          <span className="block text-[10px] text-[#94a3b8] uppercase">Review</span>
                          <span className="text-sm font-extrabold text-amber-400">
                            {cards.length - learnedCount}
                          </span>
                        </div>
                        <div className="p-2 rounded-xl bg-[#0f172a] border border-white/6">
                          <span className="block text-[10px] text-[#94a3b8] uppercase">Total</span>
                          <span className="text-sm font-extrabold text-sky-400">{cards.length}</span>
                        </div>
                      </div>
                    </div>

                    {/* Restore Deleted Cards Button */}
                    {deletedCards.length > 0 && (
                      <button
                        type="button"
                        onClick={handleRestoreDeletedCards}
                        className="w-full py-2.5 px-4 rounded-xl bg-amber-500/15 border border-amber-500/35 hover:bg-amber-500/25 text-amber-300 font-bold flex items-center justify-center gap-2 transition-all cursor-pointer"
                      >
                        <Undo2 className="w-4 h-4 text-amber-400" />
                        <span>Restore {deletedCards.length} Deleted Card{deletedCards.length > 1 ? 's' : ''}</span>
                      </button>
                    )}

                    {/* Reset Learned Progress */}
                    <button
                      type="button"
                      onClick={handleResetLearned}
                      className="w-full py-2.5 px-4 rounded-xl bg-white/6 border border-white/10 hover:bg-white/10 text-[#94a3b8] hover:text-white font-bold flex items-center justify-center gap-2 transition-all cursor-pointer"
                    >
                      <RotateCcw className="w-4 h-4" />
                      <span>Reset Learned Progress</span>
                    </button>

                    {/* Factory Reset Deck */}
                    <button
                      type="button"
                      onClick={() => {
                        if (confirm('Reset all 199 cards to default factory deck?')) {
                          handleResetToDefaultDeck();
                        }
                      }}
                      className="w-full py-2.5 px-4 rounded-xl bg-rose-950/30 border border-rose-500/30 hover:bg-rose-950/50 text-rose-300 font-bold flex items-center justify-center gap-2 transition-all cursor-pointer text-xs"
                    >
                      <Trash2 className="w-3.5 h-3.5 text-rose-400" />
                      <span>Restore Factory 199 Cards</span>
                    </button>
                  </div>
                )}
              </div>

              {/* Settings Footer */}
              <div className="p-4 border-t border-white/10 bg-[#070a13]/80">
                <button
                  type="button"
                  onClick={() => setIsMenuOpen(false)}
                  className="w-full py-3 rounded-2xl bg-gradient-to-r from-[#0284c7] to-[#0ea5e9] text-white font-extrabold text-xs shadow-lg shadow-sky-900/40 cursor-pointer"
                >
                  Done
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* VIEW 1: HOME VIEW ('home') */}
      {view === 'home' && (
        <div className="flex flex-col flex-1 h-full overflow-hidden">
          {/* Top Header */}
          <header className="flex items-center justify-between px-5 py-4 border-b border-white/10 bg-[#070a13] shrink-0">
            <button
              type="button"
              className="p-2 -ml-1 rounded-2xl text-white hover:bg-white/8 transition-colors cursor-pointer border border-white/8"
              onClick={() => setIsMenuOpen(true)}
              aria-label="Open menu"
            >
              <Menu className="w-5 h-5 text-white" />
            </button>
            <h1 className="text-lg font-extrabold text-white tracking-tight">Decks</h1>
            <div className="w-9 h-9" />
          </header>

          {/* Home Content */}
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
                className="w-full bg-[#0f172a] border border-white/10 rounded-3xl p-5 hover:border-[#38bdf8]/50 hover:bg-[#131d36] transition-all duration-200 cursor-pointer text-left group shadow-xl"
              >
                <div className="flex items-center justify-between">
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2.5">
                      <div className="w-9 h-9 rounded-2xl bg-blue-500/15 border border-blue-500/30 flex items-center justify-center text-blue-400">
                        <BookOpen className="w-4 h-4" />
                      </div>
                      <h2 className="text-xl font-extrabold text-white tracking-tight">
                        {deck.title}
                      </h2>
                    </div>
                    <p className="text-xs font-medium text-[#94a3b8] pl-11">
                      {deck.subDecks.length} Decks Available · {deck.desc}
                    </p>
                  </div>
                  <ChevronRight className="w-5 h-5 text-[#94a3b8] group-hover:text-white transition-colors group-hover:translate-x-1 duration-150" />
                </div>

                <div className="mt-4 pt-3 border-t border-white/8 flex items-center justify-between text-xs text-[#94a3b8]">
                  <span className="flex items-center gap-1.5 text-sky-400 font-bold">
                    <Layers className="w-3.5 h-3.5" />
                    Multilingual Decks
                  </span>
                  <span className="font-mono text-white/80">{cards.length} cards</span>
                </div>
              </div>
            ))}

            {/* Add Section Button */}
            <button
              type="button"
              onClick={() => showToast('New vocabulary section added')}
              className="w-full py-4 px-4 rounded-3xl bg-transparent border border-dashed border-white/20 text-[#94a3b8] text-xs font-bold flex items-center justify-center gap-2 hover:border-[#38bdf8] hover:text-white hover:bg-[#38bdf8]/8 transition-all cursor-pointer"
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
          <header className="flex items-center justify-between px-5 py-4 border-b border-white/10 bg-[#070a13] shrink-0">
            <button
              type="button"
              className="flex items-center gap-1.5 text-xs font-bold text-[#94a3b8] hover:text-white transition-colors cursor-pointer px-3 py-1.5 rounded-xl bg-white/5 border border-white/8"
              onClick={() => setView('home')}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Decks</span>
            </button>
            <h1 className="text-base font-extrabold text-white tracking-tight">3K Vocabulary</h1>
            <button
              type="button"
              onClick={() => showToast('Section settings')}
              className="text-xs font-bold px-3 py-1.5 rounded-xl border border-white/10 text-[#94a3b8] hover:text-white cursor-pointer bg-white/5"
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
                    setView('flashcard');
                  }}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      setView('flashcard');
                    }
                  }}
                  className={`w-full bg-[#0f172a] border rounded-3xl p-5 transition-all duration-200 cursor-pointer text-left group shadow-xl ${
                    isActive
                      ? 'border-[#38bdf8]/60 hover:border-[#38bdf8] bg-[#111c36]'
                      : 'border-white/10 hover:border-white/25'
                  }`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <h3 className="text-base font-bold text-white tracking-tight">
                        {subDeck.title}
                      </h3>
                      {isActive && (
                        <span className="text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded-full bg-[#0284c7] text-white">
                          Active
                        </span>
                      )}
                    </div>
                    <ChevronRight className="w-4 h-4 text-[#94a3b8] group-hover:text-white transition-colors" />
                  </div>

                  <div className="w-full h-1.5 bg-[#1e293b] rounded-full overflow-hidden mb-2.5">
                    <div
                      className={`h-full rounded-full transition-all ${
                        isActive ? 'bg-[#38bdf8]' : 'bg-[#10b981]'
                      }`}
                      style={{ width: `${learnedRatio}%` }}
                    />
                  </div>

                  <div className="flex items-center justify-between text-xs text-[#94a3b8]">
                    <span>{subDeck.category || 'General Vocabulary'}</span>
                    <span className="font-semibold text-white/90">{cards.length} cards</span>
                  </div>
                </div>
              );
            })}

            {/* Add Sub-section Button */}
            <button
              type="button"
              onClick={() => showToast('Sub-section added')}
              className="w-full py-4 px-4 rounded-3xl bg-transparent border border-dashed border-white/20 text-[#94a3b8] text-xs font-bold flex items-center justify-center gap-2 hover:border-[#38bdf8] hover:text-white hover:bg-[#38bdf8]/8 transition-all cursor-pointer"
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
          {/* Flashcard Screen Header */}
          <header className="flex items-center justify-between px-4 py-3 border-b border-white/10 bg-[#070a13] shrink-0">
            <button
              type="button"
              className="flex items-center gap-1.5 text-xs font-bold text-[#94a3b8] hover:text-white transition-colors cursor-pointer px-2.5 py-1.5 rounded-xl bg-white/5 border border-white/8"
              onClick={() => setView('subsections')}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Decks</span>
            </button>

            {/* Card Index / Total Tracker */}
            <div className="text-xs font-bold tabular-nums text-[#94a3b8] flex items-center gap-1.5">
              <span className="px-2.5 py-1 rounded-xl bg-[#0f172a] border border-white/10 text-white font-mono">
                #{currentCard?.num || 800}
              </span>
              <span className="text-[11px] text-[#64748b]">
                ({currentIndex + 1} / {cards.length})
              </span>
            </div>

            {/* Action Buttons: Shuffle & Settings */}
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                className="p-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/8 text-[#94a3b8] hover:text-white transition-colors cursor-pointer"
                onClick={handleShuffle}
                title="Shuffle deck"
              >
                <Shuffle className="w-4 h-4" />
              </button>
              <button
                type="button"
                className="p-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/8 text-[#94a3b8] hover:text-white transition-colors cursor-pointer"
                onClick={() => setIsMenuOpen(true)}
                title="Deck Settings"
              >
                <Settings className="w-4 h-4 text-[#38bdf8]" />
              </button>
            </div>
          </header>

          {/* Slim Progress Bar */}
          <div className="w-full h-1 bg-white/6 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-[#38bdf8] via-[#818cf8] to-[#10b981] transition-all duration-200"
              style={{
                width: `${Math.round(((currentIndex + 1) / (cards.length || 1)) * 100)}%`,
              }}
            />
          </div>

          {/* Flashcard Stage with Framer-Motion Slide Transition */}
          <div className="flex-1 flex flex-col justify-center items-center px-4 py-2 overflow-hidden relative">
            <div className="relative w-full max-w-[420px] aspect-[3/4.2] max-h-[510px] perspective-1000">
              <AnimatePresence mode="popLayout" custom={direction} initial={false}>
                <motion.div
                  key={currentCard.num}
                  custom={direction}
                  variants={slideVariants}
                  initial="enter"
                  animate="center"
                  exit="exit"
                  drag="x"
                  dragConstraints={{ left: 0, right: 0 }}
                  dragElastic={0.65}
                  onDragEnd={(_, { offset, velocity }) => {
                    const swipeThreshold = 50;
                    const velocityThreshold = 350;
                    if (offset.x < -swipeThreshold || velocity.x < -velocityThreshold) {
                      handleNext();
                    } else if (offset.x > swipeThreshold || velocity.x > velocityThreshold) {
                      handlePrev();
                    }
                  }}
                  className="w-full h-full relative cursor-pointer select-none"
                  onClick={handleCardTap}
                >
                  <motion.div
                    animate={{ rotateY: isFlipped ? 180 : 0 }}
                    transition={{ duration: 0.38, ease: [0.23, 1, 0.32, 1] }}
                    style={{ transformStyle: 'preserve-3d' }}
                    className="w-full h-full relative"
                  >
                    {/* ================= FRONT FACE ================= */}
                    <div
                      style={{ backfaceVisibility: 'hidden' }}
                      className={`absolute inset-0 rounded-[28px] p-4 sm:p-5 flex flex-col justify-between shadow-2xl transition-all duration-200 border ${
                        isCurrentLearned
                          ? 'bg-gradient-to-b from-[#0c1829] to-[#091522] border-emerald-500/40 shadow-emerald-950/20'
                          : 'bg-gradient-to-b from-[#0f172a] to-[#090e1a] border-white/12 shadow-black/80 hover:border-white/20'
                      }`}
                    >
                      {/* Top Bar of Front Face */}
                      <div className="flex items-center justify-between shrink-0">
                        <div className="flex items-center gap-1.5">
                          <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-xl bg-white/6 border border-white/10 text-white">
                            #{currentCard.num}
                          </span>
                          <span className="text-[11px] font-bold px-2.5 py-1 rounded-xl bg-white/6 border border-white/10 text-[#94a3b8] truncate max-w-[150px]">
                            {currentCard.category}
                          </span>
                        </div>

                        {/* Front Face Controls: Speak, Bookmark Learned, Delete */}
                        <div className="flex items-center gap-1.5 no-flip">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              speakWord(currentCard.word, 'en');
                            }}
                            className="p-2 rounded-xl bg-white/6 hover:bg-white/12 text-[#38bdf8] border border-white/10 transition-colors cursor-pointer"
                            title="Listen English Pronunciation"
                          >
                            <Volume2 className="w-4 h-4 text-[#38bdf8]" />
                          </button>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              toggleLearned(currentCard.num);
                            }}
                            className={`p-2 rounded-xl border transition-all cursor-pointer ${
                              isCurrentLearned
                                ? 'bg-emerald-500/25 border-emerald-400 text-emerald-300 shadow-sm shadow-emerald-500/30'
                                : 'bg-white/6 hover:bg-white/12 border-white/10 text-[#94a3b8]'
                            }`}
                            title={isCurrentLearned ? 'Marked as Learned' : 'Mark as Learned'}
                          >
                            <BookmarkCheck
                              className={`w-4 h-4 ${
                                isCurrentLearned ? 'text-emerald-300' : 'text-[#94a3b8]'
                              }`}
                            />
                          </button>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteCurrentCard();
                            }}
                            className="p-2 rounded-xl bg-white/6 hover:bg-rose-950/40 border border-white/10 text-[#94a3b8] hover:text-rose-400 transition-colors cursor-pointer"
                            title="Delete card"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>

                      {/* Photo Image with Gradient Overlay */}
                      <div className="relative w-full flex-1 max-h-[220px] rounded-2xl overflow-hidden bg-black/50 border border-white/10 flex items-center justify-center my-2 shadow-inner group">
                        {currentCard.imageUrl ? (
                          <img
                            src={currentCard.imageUrl}
                            alt={currentCard.word}
                            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                            loading="lazy"
                            onError={(e) => {
                              // On error fallback to emoji
                              (e.target as HTMLElement).style.display = 'none';
                            }}
                          />
                        ) : (
                          <span className="text-6xl">{currentCard.emoji || '✨'}</span>
                        )}
                        <div className="absolute inset-0 bg-gradient-to-t from-[#090e1a]/90 via-transparent to-transparent pointer-events-none" />
                      </div>

                      {/* Target English Word */}
                      <div className="text-center py-1">
                        <span className="text-[10px] font-extrabold uppercase tracking-widest text-[#38bdf8] block mb-0.5">
                          English
                        </span>
                        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
                          {currentCard.word}
                        </h2>
                      </div>

                      {/* Double-Tap Helper */}
                      <div className="flex items-center justify-center text-[11px] text-[#64748b] gap-1 pt-1">
                        <RotateCw className="w-3 h-3 text-[#38bdf8]/70" />
                        <span>Double-tap or tap Flip for Tamil & translations</span>
                      </div>
                    </div>

                    {/* ================= BACK FACE ================= */}
                    <div
                      style={{
                        backfaceVisibility: 'hidden',
                        transform: 'rotateY(180deg)',
                      }}
                      className="absolute inset-0 rounded-[28px] p-4 sm:p-5 flex flex-col justify-between shadow-2xl bg-gradient-to-b from-[#0c1322] to-[#070b14] border border-[#38bdf8]/30 shadow-sky-950/20"
                    >
                      {/* Top Bar of Back Face */}
                      <div className="flex items-center justify-between shrink-0">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-xl bg-white/6 border border-white/10 text-white">
                            #{currentCard.num}
                          </span>
                          <span className="px-3 py-1 rounded-xl bg-sky-950/80 border border-[#38bdf8]/40 text-[#38bdf8] text-xs font-bold uppercase tracking-wider">
                            {currentCard.word}
                          </span>
                        </div>

                        {/* Back Face Controls: Edit & Speak Tamil */}
                        <div className="flex items-center gap-1.5 no-flip">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              speakWord(currentCard.tamil, 'ta');
                            }}
                            className="p-2 rounded-xl bg-white/6 hover:bg-white/12 text-emerald-400 border border-white/10 transition-colors cursor-pointer"
                            title="Listen Tamil pronunciation"
                          >
                            <Volume2 className="w-4 h-4 text-emerald-400" />
                          </button>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              openEditModal();
                            }}
                            className="p-2 rounded-xl bg-white/6 hover:bg-white/12 text-[#94a3b8] hover:text-white border border-white/10 transition-colors cursor-pointer"
                            title="Edit Translations"
                          >
                            <Pencil className="w-4 h-4" />
                          </button>
                        </div>
                      </div>

                      {/* Native Tamil Display */}
                      <div className="w-full bg-[#0c1f2d]/90 border border-[#14b8a6]/45 rounded-2xl py-4 px-3 shadow-[0_0_24px_rgba(20,184,166,0.18)] flex flex-col items-center justify-center text-center my-1">
                        <span className="text-[10px] font-extrabold uppercase tracking-widest text-emerald-400 block mb-1">
                          தூய தமிழ் (Native Tamil)
                        </span>
                        <h2 className="tamil-font text-3xl sm:text-4xl font-extrabold text-white tracking-wide">
                          {currentCard.tamil || '—'}
                        </h2>
                      </div>

                      {/* Multilingual Grid: Spanish & Hindi */}
                      <div className="grid grid-cols-2 gap-2 my-1">
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            speakWord(currentCard.spanish, 'es');
                          }}
                          className="p-2.5 rounded-2xl bg-[#141d33] border border-white/10 hover:border-rose-500/40 text-left transition-all cursor-pointer group/tile no-flip"
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[9px] font-bold px-2 py-0.5 rounded-md bg-rose-950/80 border border-rose-500/40 text-rose-300 uppercase tracking-wider">
                              ES ESPAÑOL
                            </span>
                            <Volume2 className="w-3.5 h-3.5 text-[#64748b] group-hover/tile:text-rose-300" />
                          </div>
                          <p className="text-sm font-bold text-white tracking-tight truncate">
                            {currentCard.spanish || '—'}
                          </p>
                        </button>

                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            speakWord(currentCard.hindi, 'hi');
                          }}
                          className="p-2.5 rounded-2xl bg-[#141d33] border border-white/10 hover:border-amber-500/40 text-left transition-all cursor-pointer group/tile no-flip"
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[9px] font-bold px-2 py-0.5 rounded-md bg-amber-950/80 border border-amber-500/40 text-amber-300 uppercase tracking-wider">
                              HI हिन्दी
                            </span>
                            <Volume2 className="w-3.5 h-3.5 text-[#64748b] group-hover/tile:text-amber-300" />
                          </div>
                          <p className="text-sm font-bold text-white tracking-tight truncate">
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
                        className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 cursor-pointer hover:bg-amber-500/15 transition-all no-flip"
                      >
                        <div className="flex items-center justify-between mb-0.5">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1">
                            <Zap className="w-3 h-3 text-amber-400" />
                            Memory Trick
                          </span>
                          <Pencil className="w-3 h-3 text-amber-400/80" />
                        </div>
                        <p className="text-xs text-amber-100/90 line-clamp-2 leading-relaxed">
                          {currentCard.shortcutEs ||
                            currentCard.shortcutHi ||
                            'Tap to add a clever mnemonic trick!'}
                        </p>
                      </div>

                      {/* Flip Back Helper */}
                      <div className="flex items-center justify-center text-[11px] text-[#64748b] gap-1 pt-0.5">
                        <RotateCw className="w-3 h-3" />
                        <span>Double-tap to flip back</span>
                      </div>
                    </div>
                  </motion.div>
                </motion.div>
              </AnimatePresence>
            </div>
          </div>

          {/* Bottom Navigation & Controls */}
          <footer className="px-5 py-3 border-t border-white/10 bg-[#070a13] shrink-0 space-y-2.5">
            {/* Quick Slider Seek */}
            <div className="flex items-center gap-3">
              <span className="text-[10px] font-mono text-[#64748b]">1</span>
              <input
                type="range"
                min="0"
                max={Math.max(0, cards.length - 1)}
                value={currentIndex}
                onChange={(e) => handleJumpToCard(Number(e.target.value))}
                className="flex-1 h-1 bg-[#1e293b] rounded-full appearance-none accent-[#38bdf8] cursor-pointer"
              />
              <span className="text-[10px] font-mono text-[#64748b]">{cards.length}</span>
            </div>

            {/* Navigation Buttons: Prev, Flip, Next */}
            <div className="flex items-center justify-between gap-3">
              <button
                type="button"
                onClick={handlePrev}
                disabled={currentIndex === 0}
                className="flex-1 py-3 px-4 rounded-2xl bg-[#0f172a] border border-white/10 text-xs font-bold text-white hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-1.5 transition-all cursor-pointer shadow-lg active:scale-95"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Prev</span>
              </button>

              <button
                type="button"
                onClick={handleFlip}
                className="py-3 px-6 rounded-2xl bg-gradient-to-r from-[#0284c7] to-[#0ea5e9] hover:from-[#0369a1] hover:to-[#0284c7] text-xs font-extrabold text-white flex items-center justify-center gap-1.5 transition-all cursor-pointer shadow-lg shadow-sky-900/30 active:scale-95"
              >
                <RotateCw className="w-4 h-4" />
                <span>{isFlipped ? 'Front' : 'Flip'}</span>
              </button>

              <button
                type="button"
                onClick={handleNext}
                disabled={currentIndex === cards.length - 1}
                className="flex-1 py-3 px-4 rounded-2xl bg-[#0f172a] border border-white/10 text-xs font-bold text-white hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-1.5 transition-all cursor-pointer shadow-lg active:scale-95"
              >
                <span>Next</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </footer>
        </div>
      )}
    </div>
  );
}
