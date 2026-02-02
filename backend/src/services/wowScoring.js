/**
 * WOW Score Algorithm
 * Intelligently rates innovations based on multiple factors
 * Score range: 0-10 (represented as stars ⭐)
 */

/**
 * Calculate WOW score for an innovation
 * @param {Object} innovation - Innovation object
 * @param {Object} context - Platform context (agents, tasks, etc.)
 * @returns {number} - WOW score (0-10)
 */
export function calculateWowScore(innovation, context = {}) {
  let score = 0;

  // Factor 1: Novelty (0-3 points)
  score += assessNovelty(innovation, context);

  // Factor 2: Complexity (0-2 points)
  score += assessComplexity(innovation);

  // Factor 3: Impact Potential (0-3 points)
  score += assessImpact(innovation);

  // Factor 4: Collaboration (0-2 points)
  score += assessCollaboration(innovation);

  // Round to nearest integer
  return Math.min(Math.round(score), 10);
}

/**
 * Assess innovation novelty
 */
function assessNovelty(innovation, context) {
  const { innovations = [] } = context;
  let noveltyScore = 2; // Base score

  const title = innovation.title.toLowerCase();
  const category = innovation.category?.toLowerCase() || '';

  // Check uniqueness
  const similarInnovations = innovations.filter(inn => {
    if (inn.id === innovation.id) return false;

    const innTitle = inn.title.toLowerCase();
    const innCategory = inn.category?.toLowerCase() || '';

    // Check title similarity
    const titleWords = new Set(title.split(' ').filter(w => w.length > 3));
    const innTitleWords = new Set(innTitle.split(' ').filter(w => w.length > 3));
    const commonWords = [...titleWords].filter(w => innTitleWords.has(w));

    // Check category match
    const categoryMatch = category && innCategory && category === innCategory;

    return commonWords.length > 1 || categoryMatch;
  });

  // More unique = higher score
  if (similarInnovations.length === 0) {
    noveltyScore += 1; // Completely unique
  } else if (similarInnovations.length === 1) {
    noveltyScore += 0.5; // Somewhat unique
  }

  // Bonus for breakthrough keywords
  const breakthroughKeywords = [
    'breakthrough', 'revolutionary', 'novel', 'unprecedented',
    'groundbreaking', 'innovative', 'disruptive', 'quantum'
  ];

  const hasBreakthroughKeyword = breakthroughKeywords.some(keyword =>
    title.includes(keyword) || innovation.description?.toLowerCase().includes(keyword)
  );

  if (hasBreakthroughKeyword) {
    noveltyScore += 0.5;
  }

  return Math.min(noveltyScore, 3);
}

/**
 * Assess innovation complexity
 */
function assessComplexity(innovation) {
  let complexityScore = 1; // Base score

  const description = innovation.description || '';
  const outputData = innovation.output_data || {};

  // Length indicates complexity
  if (description.length > 500) {
    complexityScore += 0.5;
  }

  // Check for technical depth
  const technicalKeywords = [
    'algorithm', 'architecture', 'system', 'framework', 'pipeline',
    'optimization', 'machine learning', 'ai', 'distributed', 'scalable',
    'real-time', 'microservices', 'neural', 'quantum', 'blockchain'
  ];

  const technicalDepth = technicalKeywords.filter(keyword =>
    description.toLowerCase().includes(keyword)
  ).length;

  complexityScore += Math.min(technicalDepth * 0.2, 0.5);

  // Output data richness
  const outputKeys = Object.keys(outputData);
  if (outputKeys.length > 5) {
    complexityScore += 0.3;
  }

  return Math.min(complexityScore, 2);
}

/**
 * Assess potential impact
 */
function assessImpact(innovation) {
  let impactScore = 1.5; // Base score

  const title = innovation.title.toLowerCase();
  const description = innovation.description?.toLowerCase() || '';

  // High-impact categories
  const highImpactCategories = [
    'ai', 'machine-learning', 'automation', 'security', 'healthcare',
    'education', 'climate', 'energy', 'transportation'
  ];

  if (highImpactCategories.some(cat =>
    innovation.category?.toLowerCase().includes(cat)
  )) {
    impactScore += 0.5;
  }

  // Impact keywords
  const impactKeywords = [
    'solve', 'improve', 'optimize', 'automate', 'transform',
    'revolutionize', 'enhance', 'accelerate', 'scale', 'efficiency'
  ];

  const hasImpactKeyword = impactKeywords.some(keyword =>
    title.includes(keyword) || description.includes(keyword)
  );

  if (hasImpactKeyword) {
    impactScore += 0.5;
  }

  // Scope indicators
  const scopeKeywords = ['platform', 'system', 'ecosystem', 'network', 'global'];
  const hasScope = scopeKeywords.some(keyword =>
    title.includes(keyword) || description.includes(keyword)
  );

  if (hasScope) {
    impactScore += 0.5;
  }

  return Math.min(impactScore, 3);
}

/**
 * Assess collaboration level
 */
function assessCollaboration(innovation) {
  let collabScore = 0.5; // Base score

  const agentsInvolved = innovation.agents_involved || [];

  // More agents = better collaboration
  if (agentsInvolved.length >= 2) {
    collabScore += 0.5;
  }

  if (agentsInvolved.length >= 3) {
    collabScore += 0.5;
  }

  if (agentsInvolved.length >= 5) {
    collabScore += 0.5; // Swarm innovation!
  }

  return Math.min(collabScore, 2);
}

/**
 * Get star representation of WOW score
 */
export function getStarRating(score) {
  return '⭐'.repeat(Math.min(score, 10));
}

/**
 * Get WOW level description
 */
export function getWowLevel(score) {
  if (score >= 9) return '🚀 LEGENDARY';
  if (score >= 7) return '✨ AMAZING';
  if (score >= 5) return '👍 IMPRESSIVE';
  if (score >= 3) return '👌 GOOD';
  return '🌱 PROMISING';
}

/**
 * Update innovation with calculated WOW score
 */
export function scoreInnovation(innovation, context = {}) {
  const wowScore = calculateWowScore(innovation, context);
  const starRating = getStarRating(wowScore);
  const wowLevel = getWowLevel(wowScore);

  return {
    ...innovation,
    wow_score: wowScore,
    star_rating: starRating,
    wow_level: wowLevel
  };
}

export default {
  calculateWowScore,
  getStarRating,
  getWowLevel,
  scoreInnovation
};
