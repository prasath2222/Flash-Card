# Security Specification & Red Team Audit

## Data Invariants
1. **Identity Integrity**: A user profile under `/users/{userId}` can only be created, read, or modified by the authenticated user whose `request.auth.uid == userId`.
2. **Schema Containment**: No shadow or unauthorized administrative fields (e.g., `isAdmin`, `role`) can be injected into user profile documents (`hasOnly` strict allowlists).
3. **Immutability of Identity**: `userId` is strictly immutable on update; a user cannot alter the ownership of their profile or transfer their shortcuts to another account.
4. **Isolated Personal Data**: Custom card shortcuts under `/users/{userId}/customShortcuts/{cardNum}` belong strictly to the owning user; cross-user reading and cross-user writes are categorically rejected.

## The "Dirty Dozen" Threat Payloads & Test Results
1. **Unauthenticated Read on `/users/alice`**: Returns `PERMISSION_DENIED` (Default-deny catches unauthenticated queries).
2. **Bob attempting to read Alice's profile `/users/alice`**: Returns `PERMISSION_DENIED` (`isOwner(userId)` checks `request.auth.uid == 'alice'`).
3. **Bob attempting to write into Alice's profile `/users/alice`**: Returns `PERMISSION_DENIED` (`request.auth.uid != 'alice'`).
4. **Alice attempting to spoof ownership with mismatched body (`userId: 'bob'`)**: Returns `PERMISSION_DENIED` (`incoming().userId == request.auth.uid`).
5. **Alice attempting to inject ghost field (`isAdmin: true`)**: Returns `PERMISSION_DENIED` (`hasOnly` key constraint).
6. **Alice attempting to mutate `userId` on update**: Returns `PERMISSION_DENIED` (`incoming().userId == existing().userId`).
7. **Listing all users `/users`**: Returns `PERMISSION_DENIED` (`allow list: if false`).
8. **Unauthenticated write to `/test/connection`**: Returns `PERMISSION_DENIED` (`write: if false`).
9. **Bob attempting to read Alice's custom shortcuts `/users/alice/customShortcuts/800`**: Returns `PERMISSION_DENIED` (`isOwner(userId)`).
10. **Bob attempting to update Alice's custom shortcuts `/users/alice/customShortcuts/800`**: Returns `PERMISSION_DENIED` (`isOwner(userId)`).
11. **Malicious document ID injection exceeding 128 bytes**: Returns `PERMISSION_DENIED` (`isValidId(id)`).
12. **Alice attempting to write negative or oversized shortcut text**: Protected by frontend validation and field bounds.
