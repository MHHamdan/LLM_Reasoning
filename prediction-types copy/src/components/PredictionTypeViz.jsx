import React from 'react';

const PredictionTypeViz = () => {
  const PatternVisualization = ({ pattern }) => {
    return (
      <div className="inline-block">
        <div className="grid grid-cols-6 gap-0.5" style={{ width: '150px', height: '150px' }}>
          {pattern.map((row, i) => (
            row.map((cell, j) => (
              <div
                key={`${i}-${j}`}
                className={`w-full h-full ${
                  cell === 'filled' ? 'bg-blue-600' :
                  cell === 'current' ? 'bg-red-500' :
                  'bg-gray-200'
                }`}
                style={{ aspectRatio: '1' }}
              />
            ))
          ))}
        </div>
      </div>
    );
  };

  const types = [
    {
      title: 'Left-to-right Autoregressive Prediction',
      formula: 'P(X) = ∏|X|ᵢ₌₁ P(xᵢ|x₁,...,xᵢ₋₁)',
      description: 'Predicts each token based on all previous tokens in the sequence.',
      examples: 'RNN, Transformer LM',
      details: 'Processes input sequentially from left to right, with each prediction depending on all previous elements.',
      complexity: 'O(n) for generation, where n is sequence length',
      limitations: 'Cannot utilize future context, sequential generation can be slow',
      pattern: Array(6).fill(null).map((_, i) => 
        Array(6).fill(null).map((_, j) => j <= i ? 'filled' : 'empty')
      )
    },
    {
      title: 'Left-to-right Markov Chain (order n-1)',
      formula: 'P(X) = ∏|X|ᵢ₌₁ P(xᵢ|xᵢ₋ₙ₊₁,...,xᵢ₋₁)',
      description: 'Predicts based on a fixed window of previous tokens.',
      examples: 'n-gram LM, feed-forward LM',
      details: 'Limited context window reduces complexity but may miss long-range dependencies',
      complexity: 'O(1) per token, fixed context window',
      limitations: 'Fixed context window may miss important long-range patterns',
      pattern: Array(6).fill(null).map((_, i) => 
        Array(6).fill(null).map((_, j) => {
          if (j === i) return 'current';
          if (j >= i-2 && j < i) return 'filled';
          return 'empty';
        })
      )
    },
    {
      title: 'Independent Prediction',
      formula: 'P(X) = ∏|X|ᵢ₌₁ P(xᵢ)',
      description: 'Treats each token as independent of others.',
      examples: 'Unigram model',
      details: 'Simplest model, no context consideration',
      complexity: 'O(1) per token, fastest prediction',
      limitations: 'Ignores all contextual relationships between tokens',
      pattern: Array(6).fill(null).map((_, i) => 
        Array(6).fill(null).map((_, j) => i === j ? 'current' : 'empty')
      )
    },
    {
      title: 'Bidirectional Prediction',
      formula: 'P(X) ≠ ∏|X|ᵢ₌₁ P(xᵢ|x≠ᵢ)',
      description: 'Uses both past and future context for predictions.',
      examples: 'Masked language model',
      details: 'Full context access enables rich understanding but requires special training',
      complexity: 'O(n) for attention-based models',
      limitations: 'Cannot be used for direct sequence generation',
      pattern: Array(6).fill(null).map(() => Array(6).fill('filled'))
    }
  ];

  return (
    <div className="max-w-5xl mx-auto p-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-12">
        Types of Unconditioned Prediction
      </h1>

      <div className="space-y-16">
        {types.map((type, index) => (
          <div key={index} className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-800">
              {type.title}
            </h2>

            <div className="text-lg font-mono">
              {type.formula}
            </div>

            <p className="text-gray-700">
              {type.description}
            </p>

            <div className="space-y-2">
              <p><span className="font-semibold">Examples:</span> {type.examples}</p>
              <p><span className="font-semibold">Technical Details:</span> {type.details}</p>
              <p><span className="font-semibold">Complexity:</span> {type.complexity}</p>
              <p><span className="font-semibold">Key Limitations:</span> {type.limitations}</p>
            </div>

            <div className="mt-6">
              <PatternVisualization pattern={type.pattern} />
            </div>
          </div>
        ))}
      </div>

      <style>{`
        @media print {
          body {
            color: black;
          }
          @page {
            margin: 2cm;
          }
        }
      `}</style>
    </div>
  );
};

export default PredictionTypeViz;