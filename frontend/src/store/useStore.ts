import { create } from 'zustand';

interface AppState {
    agents: Record<string, { status: string; currentTask: string }>;
    updateAgent: (agentId: string, status: string, currentTask: string) => void;
}

export const useStore = create<AppState>((set) => ({
    agents: {},
    updateAgent: (agentId, status, currentTask) => 
        set((state) => ({
            agents: { 
                ...state.agents, 
                [agentId]: { status, currentTask } 
            }
        })),
}));
