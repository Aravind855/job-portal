import React from 'react';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import RegisterAdmin from './components/registerAdmin';
import RegisterUser from './components/registeruser';
import LoginAdmin from './components/loginadmin';
import LoginUser from './components/loginuser';
import AdminDashboard from './components/admindashboard';
import PostJobs from './components/postjobs';
import Userdashboard from './components/userdashboard';
// import Home from './components/home';
import User from './components/user';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register-admin" element={<RegisterAdmin /> } />
        <Route path="/register-user" element={<RegisterUser />} />
        <Route path="/login-admin" element={<LoginAdmin />} />
        <Route path="/login-user" element={<LoginUser />} />
        <Route path="/admindashboard" element={<AdminDashboard />} />
        <Route path="/postjobs" element={<PostJobs />} />
        <Route path="/userdashboard" element={<Userdashboard />} />
        
        {/* <Route path="/home" element={Home} /> */}
        <Route path="/user" element={<User />} />
      </Routes>
    </Router>
  );
}

export default App;

