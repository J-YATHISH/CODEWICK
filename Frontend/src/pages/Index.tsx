
import React, { useState } from 'react';
import RoleSelector from '../components/RoleSelector';
import FarmerChat from '../components/FarmerChat';
import GardenerChat from '../components/GardenerChat';

export type UserRole = 'farmer' | 'gardener' | null;

const Index = () => {
  const [userRole, setUserRole] = useState<UserRole>(null);

  const handleRoleSelect = (role: UserRole) => {
    setUserRole(role);
  };

  const handleBackToRoleSelector = () => {
    setUserRole(null);
  };

  if (userRole === 'farmer') {
    return <FarmerChat onBack={handleBackToRoleSelector} />;
  }

  if (userRole === 'gardener') {
    return <GardenerChat onBack={handleBackToRoleSelector} />;
  }

  return <RoleSelector onRoleSelect={handleRoleSelect} />;
};

export default Index;
