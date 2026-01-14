// src/features/skills/services/index.ts
import { api } from '@/lib/api';

export interface Skill {
  id: string;
  name: string;
  description?: string;
  category?: string;
  proficiency_level: number; // 1-5 scale
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateSkillData {
  name: string;
  description?: string;
  category?: string;
  proficiency_level?: number; // 1-5 scale
}

export interface UpdateSkillData {
  name?: string;
  description?: string;
  category?: string;
  proficiency_level?: number; // 1-5 scale
}

export const skillsApi = {
  async getAll(): Promise<Skill[]> {
    return await api.get('/api/skills');
  },

  async getById(id: string): Promise<Skill> {
    return await api.get(`/api/skills/${id}`);
  },

  async create(data: CreateSkillData): Promise<Skill> {
    return await api.post('/api/skills', data);
  },

  async update(id: string, data: UpdateSkillData): Promise<Skill> {
    return await api.put(`/api/skills/${id}`, data);
  },

  async delete(id: string): Promise<{ success: boolean }> {
    return await api.delete(`/api/skills/${id}`);
  },
};