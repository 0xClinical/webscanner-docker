import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Login from './components/Login';
import Navbar from './components/Navbar';
import VulnerabilityScan from './pages/VulnerabilityScan';
import VulnerabilityInfo from './pages/VulnerabilityInfo';
import Dashboard from './pages/Dashboard';
import PhishingDetection from './pages/PhishingDetection';
import UserSettings from './pages/UserSetting'
interface ScanResult {
  type: string;
  url: string;
}
interface User {
  id: number,
  email: string,
  role: string,
  created_at: string
}
function App() {
  const [token, setToken] = useState<string | null>(null);
  const [scanResults, setScanResults] = useState<ScanResult[]>([]);
  const [scanUrl, setScanUrl] = useState('');
  const [user, setUser] = useState<any>(null);

  const handleLogin = (token: string,user: User) => {
    setToken(token);
    setUser(user);
  };
  const handleScanComplete = (results: ScanResult[], url: string) => {
    setScanResults(results);
    setScanUrl(url);
  };


  return (
    <Router>
    <div className={`App ${token ? 'logged-in' : 'logged-out'}`}>
      {token ? (
        <>
          <Navbar />
          <div className="content">
            <Routes>
            <Route 
                path="/vulnerability-scan" 
                element={<VulnerabilityScan onScanComplete={handleScanComplete} />} 
              />

            <Route 
                path="/vulnerability-info" 
                element={<VulnerabilityInfo scanResults={scanResults} scanUrl={scanUrl} />} 
              />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/phishing-detection" element={<PhishingDetection />} />
              <Route path="/user-settings" element={<UserSettings user={user} />} />
              <Route path="*" element={<Navigate to="/vulnerability-scan" />} />
            </Routes>
          </div>
        </>
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  </Router>
  );
}

export default App;
