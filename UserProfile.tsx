import React, { useState, useEffect } from 'react';

interface UserProfileProps {
  userId: string;
  userBio: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId, userBio }) => {
  const [data, setData] = useState<any>(null);
  const [scrollPosition, setScrollPosition] = useState(0);
  const [renderCount, setRenderCount] = useState(0);

  // BUG 1: Infinite loop (updating state in useEffect without dependency array)
  useEffect(() => {
    setRenderCount(renderCount + 1);
  });

  // BUG 2: Memory Leak (adding event listener without cleanup)
  useEffect(() => {
    const handleScroll = () => {
      setScrollPosition(window.scrollY);
    };
    window.addEventListener('scroll', handleScroll);
    // Missing return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    // BUG 3: Unhandled Promise Rejection (no .catch or try/catch)
    fetch(`https://api.example.com/users/${userId}`)
      .then(res => res.json())
      .then(json => {
        setData(json);
      });
  }, [userId]);

  return (
    <div className="user-profile">
      <h1>User Profile</h1>
      <p>Render Count: {renderCount}</p>
      <p>Scroll Position: {scrollPosition}</p>
      
      {/* SECURITY VULNERABILITY: XSS via dangerouslySetInnerHTML from props */}
      <div 
        className="user-bio"
        dangerouslySetInnerHTML={{ __html: userBio }} 
      />

      {data && (
        <div className="user-details">
          <p>Name: {data.name}</p>
          <p>Email: {data.email}</p>
        </div>
      )}
    </div>
  );
};
