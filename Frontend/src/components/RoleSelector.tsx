
import React from 'react';
import { UserRole } from '../pages/Index';

interface RoleSelectorProps {
  onRoleSelect: (role: UserRole) => void;
}

const RoleSelector: React.FC<RoleSelectorProps> = ({ onRoleSelect }) => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-green-100 flex flex-col items-center justify-center p-6">
      <div className="text-center mb-12">
        <div className="w-24 h-24 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <span className="text-4xl text-white">🌱</span>
        </div>
        <h1 className="text-4xl font-bold text-green-800 mb-4">
          Welcome to AgriSaarthi
        </h1>
        <p className="text-xl text-green-700 mb-8">
          Choose your role
        </p>
      </div>

      <div className="w-full max-w-md space-y-6">
        <button
          onClick={() => onRoleSelect('farmer')}
          className="w-full bg-green-600 hover:bg-green-700 text-white text-xl font-semibold py-6 px-8 rounded-2xl shadow-lg transition-all duration-200 transform hover:scale-105 active:scale-95"
        >
          <div className="flex items-center justify-center space-x-3">
            <span className="text-3xl">👨‍🌾</span>
            <span>Farmer</span>
          </div>
        </button>

        <button
          onClick={() => onRoleSelect('gardener')}
          className="w-full bg-green-500 hover:bg-green-600 text-white text-xl font-semibold py-6 px-8 rounded-2xl shadow-lg transition-all duration-200 transform hover:scale-105 active:scale-95"
        >
          <div className="flex items-center justify-center space-x-3">
            <span className="text-3xl">🌿</span>
            <span>Gardener</span>
          </div>
        </button>
      </div>

      <div className="mt-12 text-center">
        <p className="text-green-600 text-sm">
          Your AI-powered agricultural assistant
        </p>
      </div>
    </div>
  );
};

export default RoleSelector;
