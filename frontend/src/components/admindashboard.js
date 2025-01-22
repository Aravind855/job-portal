import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Button from "./ui/button";

const AdminDashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Fetch jobs from the backend
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get("http://localhost:8000/jobs/");
        if (response.data.status === "success") {
          setJobs(response.data.jobs || []);
        } else {
          setError(response.data.message || "Failed to fetch jobs.");
        }
      } catch (err) {
        setError("An error occurred while fetching job data.");
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  const styles = {
    adminDashboard: {
      minHeight: "100vh",
      backgroundColor: "#f9fafb",
    },
    container: {
      maxWidth: "1120px",
      margin: "0 auto",
      padding: "2rem",
    },
    header: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: "2rem",
    },
    title: {
      fontSize: "2rem",
      fontWeight: "bold",
      color: "#1a202c",
    },
    grid: {
      display: "grid",
      gridTemplateColumns: "repeat(1, 1fr)",
      gap: "2rem",
    },
    flashcard: {
      backgroundColor: "#fff",
      borderRadius: "0.75rem",
      padding: "1.5rem",
      boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
      transition: "transform 0.2s, box-shadow 0.2s",
      cursor: "pointer",
    },
    flashcardHover: {
      transform: "scale(1.03)",
      boxShadow: "0 6px 10px rgba(0, 0, 0, 0.15)",
    },
    cardHeader: {
      marginBottom: "1rem",
    },
    cardTitle: {
      fontSize: "1.5rem",
      fontWeight: "bold",
      color: "#2d3748",
    },
    cardContent: {
      lineHeight: "1.5",
      color: "#4a5568",
    },
    button: {
      marginTop: "1rem",
      display: "inline-block",
      backgroundColor: "#3182ce",
      color: "#fff",
      padding: "0.5rem 1rem",
      borderRadius: "0.5rem",
      textDecoration: "none",
      fontWeight: "500",
      textAlign: "center",
    },
    '@media (minWidth: 640px)': {
      grid: {
        gridTemplateColumns: "repeat(2, 1fr)",
      },
    },
    '@media (minWidth: 1024px)': {
      grid: {
        gridTemplateColumns: "repeat(3, 1fr)",
      },
    },
  };

  return (
    <div style={styles.adminDashboard}>
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>Admin Dashboard</h1>
          <Button onClick={() => navigate("/postjobs")}>
            Post New Job
          </Button>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : (
          <div style={styles.grid}>
            {jobs.length === 0 ? (
              <p>No jobs available.</p>
            ) : (
              jobs.map((job) => (
                <div
                  key={job._id}
                  style={styles.flashcard}
                  onMouseEnter={(e) =>
                    e.currentTarget.setAttribute(
                      "style",
                      Object.entries({
                        ...styles.flashcard,
                        ...styles.flashcardHover,
                      })
                        .map(([key, value]) => `${key}:${value}`)
                        .join(";")
                    )
                  }
                  onMouseLeave={(e) =>
                    e.currentTarget.setAttribute(
                      "style",
                      Object.entries(styles.flashcard)
                        .map(([key, value]) => `${key}:${value}`)
                        .join(";")
                    )
                  }
                >
                  <div style={styles.cardHeader}>
                    <h2 style={styles.cardTitle}>{job.job_title}</h2>
                  </div>
                  <div style={styles.cardContent}>
                    <p>
                      <strong>Company:</strong> {job.company}
                    </p>
                    <p>
                      <strong>Location:</strong> {job.location}
                    </p>
                    <p>
                      <strong>Qualification:</strong> {job.qualification}
                    </p>
                    <p>
                      <strong>Skills:</strong> {job.required_skills_and_qualifications}
                    </p>
                    <p>
                      <strong>Salary:</strong> {job.salary_range}
                    </p>
                  </div>
                  <a
                    href="#"
                    style={styles.button}
                    onClick={(e) => {
                      e.preventDefault();
                      alert(`View details for ${job.job_title}`);
                    }}
                  >
                    Edit Details
                  </a>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
