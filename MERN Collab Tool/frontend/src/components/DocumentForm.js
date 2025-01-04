import React, { useState } from 'react';
import { Container, Form, Button, Alert, Spinner } from 'react-bootstrap';
import axios from 'axios';

const DocumentForm = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [content, setContent] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate form fields
        if (!title || !description || !content) {
            setError('Please fill in all fields.');
            return;
        }

        setLoading(true);  // Start loading
        setError('');       // Clear any previous errors

        try {
            const newDocument = { title, description, content };

            // Send the document data to the backend
            const response = await axios.post('http://localhost:5000/api/documents', newDocument);

            // Handle success
            setLoading(false);
            setSuccess(true);
            setTitle('');
            setDescription('');
            setContent('');
        } catch (error) {
            setLoading(false);
            setError('An error occurred while saving the document.');
        }
    };

    return (
        <Container className="mt-5">
            <h2>Create New Document</h2>

            {/* Display success message */}
            {success && <Alert variant="success">Document created successfully!</Alert>}

            {/* Display error message */}
            {error && <Alert variant="danger">{error}</Alert>}

            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="title" className="mb-3">
                    <Form.Label>Document Title</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter document title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="description" className="mb-3">
                    <Form.Label>Document Description</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter document description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="content" className="mb-3">
                    <Form.Label>Document Content</Form.Label>
                    <Form.Control
                        as="textarea"
                        rows={5}
                        placeholder="Enter document content"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                    />
                </Form.Group>

                <Button variant="primary" type="submit" disabled={loading}>
                    {loading ? (
                        <Spinner animation="border" size="sm" />
                    ) : (
                        'Create Document'
                    )}
                </Button>
            </Form>
        </Container>
    );
};

export default DocumentForm;
