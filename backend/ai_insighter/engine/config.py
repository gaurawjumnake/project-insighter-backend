
TOKEN_THRESHOLD  = 6000      # compress data section if it exceeds this

# ── Output schemas ────────────────────────────────────────────
PROJECT_SCHEMA = {
  "project_id": "string",
  "project_name": "string",
  "account_id": "string",
  "delivery_unit_id": "string",

  "overall_health": {
    "score": 0,
    "classification": "healthy | stable | at_risk | critical",
    "summary": "string"
  },

  "delivery_analysis": {
    "delivery_status": "on_track | moderate_risk | high_risk | delayed",
    "timeline_health": "healthy | slipping | critical",
    "key_delivery_signals": [
      "string"
    ],
    "blockers": [
      {
        "type": "dependency | infra | resource | governance | technical | other",
        "severity": "low | medium | high",
        "description": "string",
        "evidence": "string"
      }
    ],
    "contradictions": [
      {
        "statement": "string",
        "evidence": "string",
        "impact": "string"
      }
    ]
  },

  "engineering_analysis": {
    "engineering_maturity": "leading | stable | developing | weak",
    "code_quality": {
      "coverage_pct": 0,
      "classification": "good | moderate | high_risk"
    },
    "quality_signals": [
      "string"
    ],
    "devops_maturity": "leading | stable | developing | weak",
    "qa_maturity": "leading | stable | developing | weak"
  },

  "ai_analysis": {
    "ai_maturity": "leading | stable | developing | weak",
    "ai_direct_hours": 0,
    "ai_assist_hours": 0,
    "total_ai_hours": 0,
    "utilization_effectiveness": "high | moderate | low",
    "ai_value_signals": [
      "string"
    ],
    "ai_gaps": [
      "string"
    ]
  },

  "technology_analysis": {
    "technology_profile": [
      {
        "technology": "string",
        "domain": "frontend | backend | cloud | data | ai_ml | devops | qa | security | other",
        "execution_maturity": "leading | stable | developing | weak",
        "source": "structured | inferred_sow | inferred_wsr"
      }
    ],
    "modernization_status": "modern | mixed | legacy_heavy",
    "technology_gaps": [
      "string"
    ]
  },

  "capability_evidence": [
    {
      "capability": "string",
      "evidence": "string",
      "business_impact": "string",
      "confidence": "high | medium | low"
    }
  ],

  "gap_analysis": [
    {
      "gap_type": "delivery | engineering | ai | governance | technology | automation",
      "severity": "low | medium | high",
      "description": "string",
      "business_impact": "string"
    }
  ],

  "reusable_patterns": {
    "success_patterns": [
      {
        "pattern": "string",
        "business_impact": "string",
        "applicability": "project_only | account_reusable | portfolio_reusable"
      }
    ],
    "failure_patterns": [
      {
        "pattern": "string",
        "business_impact": "string",
        "applicability": "project_only | account_reusable | portfolio_reusable"
      }
    ]
  },

  "commercial_opportunities": [
    {
      "priority": "high | medium | low",
      "gap": "string",
      "recommended_service": "string",
      "expected_outcome": "string",
      "pitch": "string"
    }
  ],

  "strategic_positioning_signals": [
    {
      "theme": "string",
      "message": "string",
      "business_value": "string"
    }
  ],

  "recommendations": [
    {
      "priority": "high | medium | low",
      "recommendation": "string",
      "expected_outcome": "string"
    }
  ]
}

ACCOUNT_SCHEMA = {
  "account_id": "string",
  "account_name": "string",

  "overall_health": {
    "score": 0,
    "classification": "healthy | stable | at_risk | critical",
    "summary": "string"
  },

  "portfolio_operational_analysis": {
    "delivery_maturity": "leading | stable | developing | weak",
    "governance_maturity": "leading | stable | developing | weak",
    "delivery_patterns": [
      {
        "pattern": "string",
        "affected_projects": [
          "string"
        ],
        "severity": "low | medium | high",
        "business_impact": "string"
      }
    ],
    "cross_project_contradictions": [
      {
        "contradiction": "string",
        "projects": [
          "string"
        ],
        "impact": "string"
      }
    ]
  },

  "financial_analysis": {
    "revenue_health": "healthy | moderate_risk | high_risk",
    "revenue_concentration_risk": "low | medium | high",
    "forecast_accuracy": "strong | moderate | weak",
    "financial_risks": [
      {
        "risk": "string",
        "affected_projects": [
          "string"
        ],
        "impact": "string"
      }
    ]
  },

  "ai_maturity_analysis": {
    "account_ai_maturity": "leading | stable | developing | weak",
    "high_maturity_projects": [
      "string"
    ],
    "low_maturity_projects": [
      "string"
    ],
    "ai_success_patterns": [
      {
        "pattern": "string",
        "source_project": "string",
        "business_impact": "string"
      }
    ],
    "ai_gap_patterns": [
      "string"
    ]
  },

  "account_capability_profile": [
    {
      "capability": "string",
      "supporting_projects": [
        "string"
      ],
      "business_value": "string",
      "maturity": "leading | stable | developing | weak"
    }
  ],

  "cross_project_replication_opportunities": [
    {
      "source_project": "string",
      "target_projects": [
        "string"
      ],
      "practice": "string",
      "expected_benefit": "string",
      "implementation_complexity": "low | medium | high"
    }
  ],

  "cross_project_failure_patterns": [
    {
      "pattern": "string",
      "affected_projects": [
        "string"
      ],
      "business_impact": "string"
    }
  ],

  "transformation_opportunities": [
    {
      "opportunity": "string",
      "affected_projects": [
        "string"
      ],
      "business_outcome": "string",
      "priority": "high | medium | low"
    }
  ],

  "account_gap_analysis": [
    {
      "gap": "string",
      "affected_projects": [
        "string"
      ],
      "severity": "low | medium | high",
      "business_impact": "string"
    }
  ],

  "strategic_positioning_signals": [
    {
      "theme": "string",
      "message": "string",
      "proof_projects": [
        "string"
      ]
    }
  ],

  "commercial_growth_opportunities": [
    {
      "opportunity": "string",
      "target_projects": [
        "string"
      ],
      "recommended_capability": "string",
      "expected_business_outcome": "string",
      "priority": "high | medium | low"
    }
  ],

  "executive_recommendations": [
    {
      "priority": "high | medium | low",
      "recommendation": "string",
      "rationale": "string",
      "expected_outcome": "string"
    }
  ]
}

PE_SCHEMA = {
  "pe_name": "string",

  "portfolio_summary": {
    "portfolio_health": "healthy | stable | at_risk | fragmented",
    "transformation_maturity": "leading | stable | developing | weak",
    "summary": "string"
  },

  "portfolio_operational_analysis": {
    "portfolio_patterns": [
      {
        "pattern": "string",
        "affected_accounts": [
          "string"
        ],
        "severity": "low | medium | high",
        "business_impact": "string"
      }
    ],
    "portfolio_contradictions": [
      {
        "contradiction": "string",
        "affected_accounts": [
          "string"
        ],
        "impact": "string"
      }
    ]
  },

  "pe_strategy_alignment": {
    "aligned_areas": [
      "string"
    ],
    "misaligned_areas": [
      {
        "strategy_goal": "string",
        "portfolio_gap": "string",
        "affected_accounts": [
          "string"
        ]
      }
    ]
  },

  "portfolio_capability_profile": [
    {
      "capability": "string",
      "supporting_accounts": [
        "string"
      ],
      "business_value": "string",
      "maturity": "leading | stable | developing | weak",
      "portfolio_scalability": "low | medium | high"
    }
  ],

  "replicable_success_models": [
    {
      "source_account": "string",
      "target_accounts": [
        "string"
      ],
      "success_pattern": "string",
      "business_outcome": "string",
      "replicability": "low | medium | high"
    }
  ],

  "portfolio_failure_patterns": [
    {
      "pattern": "string",
      "affected_accounts": [
        "string"
      ],
      "business_impact": "string"
    }
  ],

  "portfolio_standardisation_opportunities": [
    {
      "opportunity": "string",
      "affected_accounts": [
        "string"
      ],
      "standardization_area": "string",
      "expected_business_outcome": "string",
      "priority": "high | medium | low"
    }
  ],

  "investment_risk_signals": [
    {
      "risk": "string",
      "affected_accounts": [
        "string"
      ],
      "risk_level": "low | medium | high",
      "business_impact": "string"
    }
  ],

  "portfolio_gap_analysis": [
    {
      "gap": "string",
      "affected_accounts": [
        "string"
      ],
      "severity": "low | medium | high",
      "business_impact": "string"
    }
  ],

  "capability_to_opportunity_mapping": [
    {
      "gap": "string",
      "company_capability": "string",
      "transformation_approach": "string",
      "expected_business_outcome": "string"
    }
  ],

  "portfolio_transformation_themes": [
    {
      "theme": "string",
      "supporting_accounts": [
        "string"
      ],
      "business_value": "string"
    }
  ],

  "strategic_positioning_signals": [
    {
      "theme": "string",
      "message": "string",
      "proof_accounts": [
        "string"
      ]
    }
  ],

  "executive_transformation_narratives": [
    {
      "narrative": "string",
      "target_audience": "PE leadership | portfolio CTO | portfolio CEO",
      "business_outcome": "string"
    }
  ],

  "leadership_pitches": [
    {
      "priority": "high | medium | low",
      "source_account": "string",
      "target_accounts": [
        "string"
      ],
      "pitch": "string",
      "proof_point": "string",
      "expected_business_outcome": "string"
    }
  ],

  "strategic_recommendations": [
    {
      "priority": "high | medium | low",
      "recommendation": "string",
      "rationale": "string",
      "expected_business_outcome": "string"
    }
  ]
}
 

ANY_DOCUMENT_SCHEMA = {"mode":"markdown"}

SCHEMAS = {
    "project":        PROJECT_SCHEMA,
    "account":        ACCOUNT_SCHEMA,
    "private_equity": PE_SCHEMA,
    "any_document":   ANY_DOCUMENT_SCHEMA
}