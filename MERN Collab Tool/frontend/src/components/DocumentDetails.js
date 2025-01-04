import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';

const DocumentDetails = ({ documentId }) => {
    const [document, setDocument] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Fetch document details when the component mounts
    useEffect(() => {
        const fetchDocumentDetails = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/api/documents/${documentId}`);
                setDocument(response.data);
                setLoading(false);
            } catch (err) {
                setError('Error fetching document details.');
                setLoading(false);
            }
        };

        fetchDocumentDetails();
    }, [documentId]);

    // If still loading, show spinner
    if (loading) {
        return (
            <Container className="text-center mt-5">
                <Spinner animation="border" variant="primary" />
                <p>Loading document details...</p>
            </Container>
        );
    }

    // If there is an error, show error message
    if (error) {
        return (
            <Container className="mt-5">
                <Alert variant="danger">{error}</Alert>
            </Container>
        );
    }

    // Render document details if data is available
    return (
        <Container className="mt-5">
            <Row>
                <Col md={8} className="offset-md-2">
                    <Card>
                        <Card.Header as="h5">Document Details</Card.Header>
                        <Card.Body>
                            <h4>{document.title}</h4>
                            <p><strong>Author:</strong> {document.author}</p>
                            <p><strong>Created On:</strong> {new Date(document.createdAt).toLocaleDateString()}</p>
                            <p><strong>Last Updated:</strong> {new Date(document.updatedAt).toLocaleDateString()}</p>
                            <hr />
                            <h5>Description:</h5>
                            <p>{document.description}</p>

                            <Button variant="warning" className="mr-2">Edit Document</Button>
                            <Button variant="danger">Delete Document</Button>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default DocumentDetails;
