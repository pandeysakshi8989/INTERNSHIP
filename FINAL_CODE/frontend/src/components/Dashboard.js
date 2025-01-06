import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css'; // Import custom CSS for styling

const Dashboard = () => {
    const [documents, setDocuments] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const user = JSON.parse(localStorage.getItem('user'));
                const token = user ? user.token : null;
                const { data } = await axios.get('http://localhost:5000/api/documents', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setDocuments(data);
            } catch (error) {
                console.error('Failed to fetch documents:', error);
                navigate('/');
            }
        };
        fetchDocuments();
    }, [navigate]);

    return (
        <div className="dashboard-container">
            <h2 className="dashboard-title">Your Documents</h2>
            <div className="document-cards">
                {documents.map((doc) => (
                    <div key={doc._id} className="card-container">
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title">{doc.title}</h5>
                                <p className="card-date">Created on: {new Date(doc.createdAt).toLocaleDateString()}</p>
                                <Link to={`/document/${doc._id}`} className="btn btn-primary mt-auto">Open Document</Link>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="text-center mt-4">
                <button className="btn btn-success create-btn" onClick={() => navigate('/document/new')}>Create New Document</button>
            </div>
        </div>
    );
};

export default Dashboard;
