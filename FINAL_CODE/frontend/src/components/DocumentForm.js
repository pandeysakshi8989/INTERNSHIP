import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './DocumentForm.css';  // Import custom CSS for styling

const DocumentForm = () => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const user = JSON.parse(localStorage.getItem('user'));
            const token = user ? user.token : null;
            const { data } = await axios.post('http://localhost:5000/api/documents', { title, content }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            navigate(`/document/${data._id}`, { state: { message: 'Document created successfully!' } });
        } catch (error) {
            console.error('Failed to create document:', error);
        }
    };

    return (
        <div className="document-form-container">
            <h2 className="document-form-title">Create New Document</h2>
            <form onSubmit={handleSubmit} className="document-form">
                <div className="form-group">
                    <label htmlFor="title" className="form-label">Title</label>
                    <input
                        type="text"
                        id="title"
                        className="form-control"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="content" className="form-label">Content</label>
                    <textarea
                        id="content"
                        className="form-control"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Create Document</button>
            </form>
        </div>
    );
};

export default DocumentForm;
