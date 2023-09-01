// public/app.js
import { getCSRFToken } from '../src/csrf.js';

// Now you can use the getCSRFToken function here or in other modules loaded from the public directory
// For example:
console.log('CSRF Token:', getCSRFToken());