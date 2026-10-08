import React from 'react';

function UserProfile({ userData }) {
  // CRITICAL: DOM XSS Vulnerability
  // Rendering raw HTML directly from user input without sanitization
  return (
    <div className="profile">
      <h1>User Profile</h1>
      <div dangerouslySetInnerHTML={{ __html: userData.bio }} />
      
      {/* BUG: Missing alt attribute for accessibility */}
      <img src={userData.avatarUrl} />
    </div>
  );
}

export default UserProfile;
