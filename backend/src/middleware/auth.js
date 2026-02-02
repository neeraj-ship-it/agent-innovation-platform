import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'amaip-secret-key-change-in-production';

export function generateToken(agentId, agentName) {
  return jwt.sign(
    { agentId, agentName },
    JWT_SECRET,
    { expiresIn: '7d' }
  );
}

export function verifyToken(token) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (err) {
    return null;
  }
}

export function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'No authentication token provided' });
  }

  const decoded = verifyToken(token);
  if (!decoded) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }

  req.agent = decoded;
  next();
}

export function optionalAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (token) {
    const decoded = verifyToken(token);
    if (decoded) {
      req.agent = decoded;
    }
  }

  next();
}

// Rate limiting
const requestCounts = new Map();

export function rateLimit(maxRequests = 100, windowMs = 60000) {
  return (req, res, next) => {
    const key = req.ip || req.connection.remoteAddress;
    const now = Date.now();

    if (!requestCounts.has(key)) {
      requestCounts.set(key, []);
    }

    const requests = requestCounts.get(key);
    const recentRequests = requests.filter(time => now - time < windowMs);

    if (recentRequests.length >= maxRequests) {
      return res.status(429).json({
        error: 'Too many requests',
        retryAfter: Math.ceil(windowMs / 1000)
      });
    }

    recentRequests.push(now);
    requestCounts.set(key, recentRequests);

    next();
  };
}

// API key validation for external agents
export function validateApiKey(req, res, next) {
  const apiKey = req.headers['x-api-key'];

  // In production, check against database
  // For now, allow all or check environment variable
  const validKeys = process.env.VALID_API_KEYS?.split(',') || [];

  if (validKeys.length > 0 && !validKeys.includes(apiKey)) {
    return res.status(403).json({ error: 'Invalid API key' });
  }

  next();
}
