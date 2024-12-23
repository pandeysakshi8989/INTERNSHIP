const mongoose = require('mongoose');

const documentSchema = new mongoose.Schema({
    title: {
        type: String,
        required: [true, 'Document title is required'],
        trim: true,
        maxlength: [100, 'Document title cannot exceed 100 characters'],
    },
    content: {
        type: String,
        required: [true, 'Document content is required'],
        minlength: [10, 'Document content must be at least 10 characters long'],
    },
    owner: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
    },
    collaborators: [
        {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User',
        },
    ],
    createdAt: {
        type: Date,
        default: Date.now,
        immutable: true,
    },
    updatedAt: {
        type: Date,
        default: Date.now,
    },
    isArchived: {
        type: Boolean,
        default: false,
    },
});

// Middleware to update the `updatedAt` field before saving
documentSchema.pre('save', function (next) {
    if (this.isModified()) {
        this.updatedAt = Date.now();
    }
    next();
});

// Add a virtual field to return a collaborator count
documentSchema.virtual('collaboratorCount').get(function () {
    return this.collaborators.length;
});

// Enable virtuals in JSON output
documentSchema.set('toJSON', { virtuals: true });
documentSchema.set('toObject', { virtuals: true });

module.exports = mongoose.model('Document', documentSchema);
