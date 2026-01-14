// src/features/skills/components/SkillsForm.tsx
import React, { useState } from 'react';
import { CreateSkillData, UpdateSkillData, skillsApi, Skill } from '../services';

interface SkillsFormProps {
  onSkillAdded?: (skill: Skill) => void;
  onSkillUpdated?: (skill: Skill) => void;
  existingSkill?: Skill | null;
  onCancel?: () => void;
}

const SkillsForm: React.FC<SkillsFormProps> = ({
  onSkillAdded,
  onSkillUpdated,
  existingSkill = null,
  onCancel,
}) => {
  const [name, setName] = useState<string>(existingSkill?.name || '');
  const [description, setDescription] = useState<string>(existingSkill?.description || '');
  const [category, setCategory] = useState<string>(existingSkill?.category || '');
  const [proficiencyLevel, setProficiencyLevel] = useState<number>(existingSkill?.proficiency_level || 3);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (existingSkill) {
        // Update existing skill
        const updatedSkill = await skillsApi.update(existingSkill.id, {
          name,
          description: description || undefined,
          category: category || undefined,
          proficiency_level: proficiencyLevel,
        } as UpdateSkillData);
        onSkillUpdated?.(updatedSkill);
      } else {
        // Create new skill
        const newSkill = await skillsApi.create({
          name,
          description: description || undefined,
          category: category || undefined,
          proficiency_level: proficiencyLevel,
        } as CreateSkillData);
        onSkillAdded?.(newSkill);
        // Reset form for new skill
        setName('');
        setDescription('');
        setCategory('');
        setProficiencyLevel(3);
      }
    } catch (err) {
      console.error('Error saving skill:', err);
      setError('Failed to save skill');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setName('');
    setDescription('');
    setCategory('');
    setProficiencyLevel(3);
    setError(null);
    onCancel?.();
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border">
      <h3 className="text-lg font-medium mb-4">
        {existingSkill ? 'Edit Skill' : 'Add New Skill'}
      </h3>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Skill Name *
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            placeholder="e.g., JavaScript, Python, Leadership"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <input
            type="text"
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Programming, Management, Design"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Describe your skill..."
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Proficiency Level
          </label>
          <div className="flex items-center">
            <div className="flex mr-2">
              {[1, 2, 3, 4, 5].map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => setProficiencyLevel(level)}
                  className={`text-2xl ${level <= proficiencyLevel ? 'text-yellow-500' : 'text-gray-300'}`}
                >
                  ★
                </button>
              ))}
            </div>
            <span className="text-sm text-gray-600 ml-2">
              {proficiencyLevel}/5
            </span>
          </div>
        </div>

        <div className="flex space-x-2">
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? 'Saving...' : (existingSkill ? 'Update Skill' : 'Add Skill')}
          </button>

          {onCancel && (
            <button
              type="button"
              onClick={handleCancel}
              className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default SkillsForm;