// src/features/skills/components/SkillsPage.tsx
import React, { useState } from 'react';
import SkillsList from './SkillsList';
import SkillsForm from './SkillsForm';
import { Skill } from '../services';

interface SkillsPageProps {
  userId: string;
}

const SkillsPage: React.FC<SkillsPageProps> = ({ userId }) => {
  const [showForm, setShowForm] = useState<boolean>(false);
  const [editingSkill, setEditingSkill] = useState<Skill | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState<number>(0);

  const handleSkillAdded = (skill: Skill) => {
    console.log('Skill added:', skill);
    setShowForm(false);
    setEditingSkill(null);
    // Trigger a refresh by changing the key
    setRefreshTrigger(prev => prev + 1);
  };

  const handleSkillUpdated = (skill: Skill) => {
    console.log('Skill updated:', skill);
    setShowForm(false);
    setEditingSkill(null);
    // Trigger a refresh by changing the key
    setRefreshTrigger(prev => prev + 1);
  };

  const handleEditSkill = (skill: Skill) => {
    setEditingSkill(skill);
    setShowForm(true);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Skills Management</h1>
        <p className="text-gray-600">Manage and track your professional skills</p>
      </div>

      <div className="mb-8">
        {!showForm ? (
          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Add New Skill
          </button>
        ) : (
          <div className="mb-8">
            <SkillsForm
              onSkillAdded={handleSkillAdded}
              onSkillUpdated={handleSkillUpdated}
              existingSkill={editingSkill}
              onCancel={() => {
                setShowForm(false);
                setEditingSkill(null);
              }}
            />
          </div>
        )}
      </div>

      <div key={`skills-list-${refreshTrigger}`}>
        <SkillsList userId={userId} />
      </div>
    </div>
  );
};

export default SkillsPage;