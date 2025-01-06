import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css'; // Don't forget to import the custom CSS

const LandingPage = () => {
    return (
        <div className="landing-page-container">
            <div className="jumbotron custom-jumbotron">
                <h1 className="display-4 custom-heading">Welcome to RealTool</h1>
                <p className="lead custom-lead">
                    RealTool is the ultimate platform for efficient and intuitive team collaboration. 
                    Work on projects, share resources, and communicate seamlessly with your colleagues in real time.
                </p>
                <hr className="custom-hr" />
                <p className="custom-description">
                    Whether you’re managing a project, brainstorming ideas, or organizing your workflow, 
                    RealTool provides all the essential tools to keep your team productive and connected.
                </p>
                <div className="button-container">
                    <Link to="/register" className="btn custom-btn-primary">Sign Up</Link>
                    <Link to="/login" className="btn custom-btn-secondary">Log In</Link>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
