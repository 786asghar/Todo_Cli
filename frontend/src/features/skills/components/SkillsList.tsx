// src/features/skills/components/SkillsList.tsx
import React, { useState, useEffect } from 'react';
import { Skill, skillsApi } from '../services';

interface SkillsListProps {
  userId: string;
}

const SkillsList: React.FC<SkillsListProps> = ({ userId }) => {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSkills();
  }, []);

  const fetchSkills = async () => {
    try {
      setLoading(true);
      const data = await skillsApi.getAll();
      setSkills(data || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching skills:', err);
      setError('Failed to fetch skills');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await skillsApi.delete(id);
      setSkills(skills.filter(skill => skill.id !== id));
    } catch (err) {
      console.error('Error deleting skill:', err);
      setError('Failed to delete skill');
    }
  };

  if (loading) {
    return <div className="text-center py-4">Loading skills...</div>;
  }

  if (error) {
    return <div className="text-red-500 py-4">{error}</div>;
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Your Skills</h2>

      {skills.length === 0 ? (
        <p className="text-gray-500">No skills added yet. Add your first skill to get started!</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {skills.map((skill) => (
            <div
              key={skill.id}
              className="border rounded-lg p-4 shadow-sm bg-white hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium text-lg">{skill.name}</h3>
                  {skill.category && (
                    <p className="text-sm text-gray-600">{skill.category}</p>
                  )}
                  {skill.description && (
                    <p className="text-sm text-gray-500 mt-1">{skill.description}</p>
                  )}
                </div>
                <button
                  onClick={() => handleDelete(skill.id)}
                  className="text-red-500 hover:text-red-700 text-sm"
                >
                  Delete
                </button>
              </div>

              <div className="mt-2">
                <div className="flex items-center">
                  <span className="text-sm mr-2">Proficiency:</span>
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <span
                        key={i}
                        className={`text-lg ${i < skill.proficiency_level ? 'text-yellow-500' : 'text-gray-300'}`}
                      >
                        ★
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="text-xs text-gray-400 mt-2">
                Updated: {new Date(skill.updated_at).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SkillsList;