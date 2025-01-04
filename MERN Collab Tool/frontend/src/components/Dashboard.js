import React from 'react';
import { Container, Row, Col, Card, Button, Navbar, Nav, Footer } from 'react-bootstrap';

function Dashboard() {
  return (
    <div>
      {/* Navbar */}
      <Navbar bg="dark" variant="dark" expand="lg">
        <Navbar.Brand href="#home">MERN Collab Tool</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#features">Features</Nav.Link>
            <Nav.Link href="#about">About</Nav.Link>
            <Nav.Link href="#contact">Contact</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>

      {/* Main Content */}
      <Container className="mt-5">
        <Row>
          {/* Dashboard Overview Card */}
          <Col md={4}>
            <Card>
              <Card.Body>
                <Card.Title>Welcome to the Dashboard</Card.Title>
                <Card.Text>
                  Manage your documents, users, and real-time collaborations here.
                </Card.Text>
                <Button variant="primary">Get Started</Button>
              </Card.Body>
            </Card>
          </Col>

          {/* Recent Activity Card */}
          <Col md={4}>
            <Card>
              <Card.Body>
                <Card.Title>Recent Activity</Card.Title>
                <Card.Text>
                  View your latest document edits, comments, and more. Stay up-to-date!
                </Card.Text>
                <Button variant="secondary">View Activity</Button>
              </Card.Body>
            </Card>
          </Col>

          {/* Notifications Card */}
          <Col md={4}>
            <Card>
              <Card.Body>
                <Card.Title>Notifications</Card.Title>
                <Card.Text>
                  Check the latest notifications and alerts related to your documents.
                </Card.Text>
                <Button variant="info">View Notifications</Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <Row className="mt-4">
          {/* Stats or Metrics Cards */}
          <Col md={6}>
            <Card>
              <Card.Body>
                <Card.Title>Document Stats</Card.Title>
                <Card.Text>
                  Track the number of documents created, edited, and shared.
                </Card.Text>
                <Button variant="warning">View Stats</Button>
              </Card.Body>
            </Card>
          </Col>

          <Col md={6}>
            <Card>
              <Card.Body>
                <Card.Title>User Activity</Card.Title>
                <Card.Text>
                  See how active your users are with document edits and comments.
                </Card.Text>
                <Button variant="success">View User Activity</Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>

      {/* Footer */}
      <footer className="bg-dark text-white py-4 mt-5">
        <Container className="text-center">
          <p>&copy; 2025 MERN Collab Tool | All Rights Reserved</p>
        </Container>
      </footer>
    </div>
  );
}

export default Dashboard;
