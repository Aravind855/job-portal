import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Button from "./ui/button";

import '../App.css'; // Update the path to point to the correct location

const PostJobs = () => {
  const navigate = useNavigate();
  const [adminData, setAdminData] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    location: "",
    qualification: "",
    job_description: "",
    required_skills_and_qualifications: "",
    salary_range: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    // Check if admin is logged in
    const storedAdminData = localStorage.getItem('adminData');
    if (!storedAdminData) {
      navigate('/login-admin');
      return;
    }

    setAdminData(JSON.parse(storedAdminData));
  }, [navigate]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/postjobs/",
        formData,
        {
          headers: {
            'X-User-Email': adminData.email,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.status === "success") {
        setSuccess("Job posted successfully!");
        // Clear form
        setFormData({
          title: "",
          location: "",
          qualification: "",
          job_description: "",
          required_skills_and_qualifications: "",
          salary_range: "",
        });
        // Redirect to dashboard after 2 seconds
        setTimeout(() => {
          navigate("/admindashboard");
        }, 2000);
      } else {
        setError(response.data.message || "Failed to post job.");
      }
    } catch (err) {
      console.error('Error details:', err.response?.data || err.message);
      setError(err.response?.data?.message || "An error occurred while posting the job. Please try again.");
    }
  };

  const styles = {
    container: {
      minHeight: "100vh",
      backgroundColor: "#f9fafb",
      padding: "2rem",
    },
    form: {
      maxWidth: "800px",
      margin: "0 auto",
      backgroundColor: "#ffffff",
      padding: "2rem",
      borderRadius: "0.75rem",
      boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    },
    title: {
      fontSize: "1.875rem",
      fontWeight: "bold",
      color: "#1a202c",
      marginBottom: "2rem",
      textAlign: "center",
    },
    companyInfo: {
      marginBottom: "2rem",
      padding: "1rem",
      backgroundColor: "#f8fafc",
      borderRadius: "0.5rem",
      border: "1px solid #e2e8f0",
    },
    companyName: {
      fontSize: "1.25rem",
      fontWeight: "bold",
      color: "#2d3748",
      marginBottom: "0.5rem",
    },
    formGroup: {
      marginBottom: "1.5rem",
    },
    label: {
      display: "block",
      marginBottom: "0.5rem",
      color: "#4a5568",
      fontSize: "0.875rem",
      fontWeight: "500",
    },
    input: {
      width: "100%",
      padding: "0.75rem",
      borderRadius: "0.5rem",
      border: "1px solid #e2e8f0",
      fontSize: "1rem",
      color: "#1a202c",
    },
    textarea: {
      width: "100%",
      padding: "0.75rem",
      borderRadius: "0.5rem",
      border: "1px solid #e2e8f0",
      fontSize: "1rem",
      color: "#1a202c",
      minHeight: "150px",
      resize: "vertical",
    },
    error: {
      color: "#e53e3e",
      marginTop: "0.5rem",
      fontSize: "0.875rem",
    },
    success: {
      color: "#38a169",
      marginTop: "0.5rem",
      fontSize: "0.875rem",
    },
    buttonContainer: {
      display: "flex",
      gap: "1rem",
      marginTop: "2rem",
    },
  };

  return (
    <div style={styles.container}>
      <form style={styles.form} onSubmit={handleSubmit}>
        <h1 style={styles.title}>Post a New Job</h1>

        {adminData?.company && (
          <div style={styles.companyInfo}>
            <h2 style={styles.companyName}>Posting as: {adminData.company.name}</h2>
          </div>
        )}

        <div style={styles.formGroup}>
          <label style={styles.label} htmlFor="title">Job Title</label>
          <input
            style={styles.input}
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label} htmlFor="location">Location</label>
          <input
            style={styles.input}
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label} htmlFor="qualification">Qualification Required</label>
          <input
            style={styles.input}
            type="text"
            id="qualification"
            name="qualification"
            value={formData.qualification}
            onChange={handleChange}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label} htmlFor="job_description">Job Description</label>
          <textarea
            style={styles.textarea}
            id="job_description"
            name="job_description"
            value={formData.job_description}
            onChange={handleChange}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label} htmlFor="required_skills_and_qualifications">Required Skills and Qualifications</label>
          <textarea
            style={styles.textarea}
            id="required_skills_and_qualifications"
            name="required_skills_and_qualifications"
            value={formData.required_skills_and_qualifications}
            onChange={handleChange}
            required
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label} htmlFor="salary_range">Salary Range</label>
          <input
            style={styles.input}
            type="text"
            id="salary_range"
            name="salary_range"
            value={formData.salary_range}
            onChange={handleChange}
            required
          />
        </div>

        {error && <p style={styles.error}>{error}</p>}
        {success && <p style={styles.success}>{success}</p>}

        <div style={styles.buttonContainer}>
          <Button type="submit" style={{ flex: 1 }}>
            Post Job
          </Button>
          <Button
            type="button"
            onClick={() => navigate("/admindashboard")}
            style={{ backgroundColor: "#718096", flex: 1 }}
          >
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
};

export default PostJobs;