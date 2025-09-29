import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

import { PracticeSession } from '@/models/practice';

interface PracticeStore {
  activeSession: PracticeSession | null;
}

interface PracticeStoreActions {
  setActiveSession: (session: PracticeSession | null) => void;
}

const usePracticeStore = create<PracticeStore & PracticeStoreActions>()(
  devtools((set) => ({
    activeSession: null,

    setActiveSession: (session) => set({ activeSession: session })
  }))
);

export default usePracticeStore;
