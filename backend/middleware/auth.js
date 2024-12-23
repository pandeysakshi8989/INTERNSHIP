const jwt = require('jsonwebtoken');

const verifyToken = (req, res, next) => {
    try {
        // Retrieve token from Authorization header
        const authHeader = req.header('Authorization');
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ message: 'Authorization header missing or improperly formatted' });
        }

        const token = authHeader.split(' ')[1];

        // Verify token
        const decoded = jwt.verify(token, process.env.JWT_SECRET);

        // Attach user information to request object
        req.user = decoded;

        // Proceed to the next middleware or route
        next();
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ message: 'Token has expired' });
        } else if (error.name === 'JsonWebTokenError') {
            return res.status(401).json({ message: 'Token is invalid' });
        } else {
            return res.status(500).json({ message: 'Server error during token verification' });
        }
    }
};

module.exports = { verifyToken };
