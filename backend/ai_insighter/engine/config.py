
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
  "transformation_proof_points": [
    {
      "proof_point_title": "string",
      "business_problem": "string",
      "source_projects": ["string"],
      "transformation_approach": "string",
      "capabilities_used": ["string"],
      "measurable_operational_outcomes": ["string"],
      "measurable_business_outcomes": ["string"],
      "stakeholder_relevance": ["CTO | CIO | COO | Delivery Leadership | Transformation Office"],
      "portability_to_other_accounts": "low | medium | high",
      "proof_strength": "weak | moderate | strong"
    }
  ],
  "account_archetype": {
    "primary": "transformation_leader | operationally_mature | governance_constrained | modernization_heavy | ai_emerging | delivery_risk_concentrated | innovation_focused | fragmented_engineering",
    "secondary": ["string"],
    "rationale": "string"
  },
  "buying_signal_analysis": {
    "overall_signal_strength": "weak | emerging | active | urgent",
    "signals": [
      {
        "signal": "modernization_pressure | operational_scalability_challenges | governance_instability | ai_adoption_mandate | cloud_migration_activity | delivery_instability | technical_debt_accumulation | automation_gap | cost_optimization_pressure | engineering_productivity_issue",
        "strength": "weak | emerging | active | urgent",
        "supporting_projects": ["string"],
        "business_driver": "string"
      }
    ],
    "expansion_potential": "low | medium | high",
    "additional_transformation_investment_likelihood": "low | medium | high",
    "strategic_account_growth_opportunity": "low | medium | high"
  },
  "transformation_readiness": {
    "classification": "ready | partially_ready | high_resistance_risk",
    "leadership_alignment": "strong | moderate | weak",
    "governance_maturity": "strong | moderate | weak",
    "operational_discipline": "strong | moderate | weak",
    "engineering_maturity": "strong | moderate | weak",
    "delivery_consistency": "strong | moderate | weak",
    "ai_readiness": "strong | moderate | weak",
    "modernization_readiness": "strong | moderate | weak",
    "rationale": "string"
  },
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

# Account layered schemas
ACCOUNT_OPERATIONAL_SCHEMA = {
  "overall_health": ACCOUNT_SCHEMA["overall_health"],
  "portfolio_operational_analysis": ACCOUNT_SCHEMA["portfolio_operational_analysis"],
  "financial_analysis": ACCOUNT_SCHEMA["financial_analysis"],
  "ai_maturity_analysis": ACCOUNT_SCHEMA["ai_maturity_analysis"],
}

ACCOUNT_CAPABILITY_PROOF_SCHEMA = {
  "account_capability_profile": ACCOUNT_SCHEMA["account_capability_profile"],
  "transformation_proof_points": ACCOUNT_SCHEMA["transformation_proof_points"],
}

ACCOUNT_STRATEGIC_COMMERCIAL_SCHEMA = {
  "account_archetype": ACCOUNT_SCHEMA["account_archetype"],
  "buying_signal_analysis": ACCOUNT_SCHEMA["buying_signal_analysis"],
  "transformation_readiness": ACCOUNT_SCHEMA["transformation_readiness"],
}

ACCOUNT_EXECUTIVE_SYNTHESIS_SCHEMA = {
  "cross_project_replication_opportunities": ACCOUNT_SCHEMA["cross_project_replication_opportunities"],
  "cross_project_failure_patterns": ACCOUNT_SCHEMA["cross_project_failure_patterns"],
  "transformation_opportunities": ACCOUNT_SCHEMA["transformation_opportunities"],
  "commercial_growth_opportunities": ACCOUNT_SCHEMA["commercial_growth_opportunities"],
  "strategic_positioning_signals": ACCOUNT_SCHEMA["strategic_positioning_signals"],
  "executive_recommendations": ACCOUNT_SCHEMA["executive_recommendations"],
}

# Extended PE strategy schemas (service-only, no DB persistence required)
PE_PORTFOLIO_SCHEMA = PE_SCHEMA

PE_PROOF_POINT_SCHEMA = {
  "proof_points": [
    {
      "proof_point_id": "string",
      "source_account": "string",
      "industry": "string",
      "business_problem": "string",
      "transformation_approach": "string",
      "capabilities_used": ["string"],
      "technologies_used": ["string"],
      "delivery_model": "string",
      "timeline": "string",
      "business_outcomes": ["string"],
      "operational_outcomes": ["string"],
      "financial_outcomes": ["string"],
      "stakeholder_type": ["string"],
      "reusability": "low | medium | high",
      "ideal_target_profile": ["string"],
      "proof_strength": "low | medium | high"
    }
  ]
}

PE_BUYING_SIGNAL_SCHEMA = {
  "buying_signals": [
    {
      "signal": "string",
      "affected_accounts": ["string"],
      "urgency": "low | medium | high",
      "confidence": "low | medium | high",
      "evidence": "string",
      "recommended_motion": "string"
    }
  ]
}

PE_WHITESPACE_SCHEMA = {
  "client_accounts_analysis": {
    "expansion_opportunities": [
      {
        "account_name": "string",
        "industry": "string",
        "expansion_theme": "string",
        "deeper_transformation_potential": "string",
        "risk_signals": ["string"],
        "recommended_next_step": "string"
      }
    ]
  },
  "non_client_portfolio_expansion_intelligence": {
    "targets": [
      {
        "target_company": "string",
        "industry": "string",
        "why_this_company_is_targetable": "string",
        "pain_points": ["string"],
        "capability_alignment": ["string"],
        "best_proof_point_to_use": {
          "source_client_account": "string",
          "proof_point_title": "string",
          "why_relevant": "string"
        },
        "gap_to_outcome_chain": {
          "gap": "string",
          "capability": "string",
          "proof_point": "string",
          "entry_strategy": "string",
          "expected_business_outcome": "string"
        },
        "opportunity_priority": "low | medium | high",
        "buying_signal_strength": "low | medium | high",
        "transformation_urgency": "low | medium | high",
        "likely_executive_buyers": ["string"],
        "commercial_confidence": "low | medium | high"
      }
    ]
  },
  "portfolio_wide_program_opportunities": [
    {
      "program_theme": "string",
      "repeatable_problem": "string",
      "affected_accounts": ["string"],
      "recommended_portfolio_program": "string",
      "expected_portfolio_outcome": "string",
      "priority": "high | medium | low"
    }
  ],
  "target_prioritization": {
    "highest_probability_targets": ["string"],
    "highest_urgency_targets": ["string"],
    "easiest_expansion_targets": ["string"],
    "tier_1_immediate_pursuit": ["string"],
    "tier_2_strategic_expansion": ["string"],
    "tier_3_long_term_watchlist": ["string"]
  },
  "whitespace_opportunities": [
    {
      "target_company": "string",
      "opportunity_priority": "low | medium | high",
      "buying_signal_strength": "low | medium | high",
      "transformation_urgency": "low | medium | high",
      "likely_business_problem": "string",
      "recommended_capabilities": ["string"],
      "recommended_proof_points": ["string"],
      "recommended_entry_strategy": "string",
      "land_and_expand_strategy": "string",
      "likely_executive_buyers": ["string"],
      "expected_business_outcomes": ["string"],
      "relationship_leverage": "string",
      "commercial_confidence": "low | medium | high"
    }
  ]
}

PE_EXECUTIVE_STRATEGY_SCHEMA = {
  "portfolio_themes": [
    {
      "theme": "string",
      "evidence_accounts": ["string"],
      "business_impact": "string"
    }
  ],
  "tier_1_immediate_targets": ["string"],
  "tier_2_strategic_expansion": ["string"],
  "tier_3_watchlist": ["string"],
  "executive_narratives": [
    {
      "narrative": "string",
      "audience": "PE leadership | portfolio CTO | portfolio CEO",
      "expected_outcome": "string"
    }
  ],
  "leadership_recommendations": [
    {
      "priority": "high | medium | low",
      "recommendation": "string",
      "rationale": "string",
      "expected_business_outcome": "string"
    }
  ]
}

SCHEMAS = {
    "project":        PROJECT_SCHEMA,
    "account":        ACCOUNT_SCHEMA,
    "account_operational": ACCOUNT_OPERATIONAL_SCHEMA,
    "account_capability_proof": ACCOUNT_CAPABILITY_PROOF_SCHEMA,
    "account_strategic_commercial": ACCOUNT_STRATEGIC_COMMERCIAL_SCHEMA,
    "account_executive_synthesis": ACCOUNT_EXECUTIVE_SYNTHESIS_SCHEMA,
    "private_equity": PE_SCHEMA,
    "any_document":   ANY_DOCUMENT_SCHEMA,
    "pe_portfolio": PE_PORTFOLIO_SCHEMA,
    "pe_proof_point": PE_PROOF_POINT_SCHEMA,
    "pe_buying_signal": PE_BUYING_SIGNAL_SCHEMA,
    "pe_whitespace": PE_WHITESPACE_SCHEMA,
    "pe_executive_strategy": PE_EXECUTIVE_STRATEGY_SCHEMA,
}