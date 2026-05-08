# Skill: Database Schema Analyzer

**Purpose:** Generate SQLAlchemy models with relationships, migrations, indexes, and query optimization  
**Agent:** @data-analyst  
**Duration:** 3-5 minutes

---

## QUERY PATTERN

```
@data-analyst Design schema for {entity}
with relationships to {related_entities}
where entity = [Account, Project, Document, ...]

Examples:
- Design schema for Invoice with relationships to Project and Account
- Optimize query for fetching Accounts with related Projects and Documents
- Create materialized view for ProjectMetrics aggregation
```

---

## IMPLEMENTATION

### Step 1: Create SQLAlchemy Model
Generate model with:
- Primary key (id, auto-increment)
- Foreign keys to parent entities
- Core attributes with type validation
- Audit fields (created_at, updated_at, deleted_at for soft delete)
- Relationships with back_populates

**Generated Code Template:**
```python
class Invoice(Base):
    __tablename__ = "invoice"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"))
    amount_usd = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="invoices")
    
    __table_args__ = (
        Index("idx_invoice_project_created", "project_id", "created_at"),
    )
```

### Step 2: Define Relationships
Include bidirectional relationships:
- One-to-Many (cascade delete orphans)
- Many-to-Many (junction table if needed)
- Lazy loading strategy (select, joined, subquery)

### Step 3: Add Indexes
Create indexes for:
- Foreign keys (always indexed)
- Frequently filtered columns
- Composite indexes for common queries

### Step 4: Optimize Queries
Review common queries and add:
- Eager loading (joinedload) to prevent N+1
- Materialized views for analytics
- Query result caching if applicable

### Step 5: Create Migration
Generate Alembic migration:
```python
def upgrade():
    op.create_table(
        'invoice',
        sa.Column('id', sa.Integer(), autoincrement=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('project.id')),
        sa.Column('amount_usd', sa.Float()),
        sa.Column('created_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['project_id'], ['project.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_invoice_project_created', 'invoice', ['project_id', 'created_at'])
```

### Step 6: Test Schema
- Validate foreign key cascades
- Test soft delete behavior
- Query performance benchmark
- Check for N+1 issues

---

## SUCCESS METRICS

- ✅ Model follows SQLAlchemy patterns
- ✅ Relationships bidirectional with back_populates
- ✅ Indexes cover >90% of queries
- ✅ Query performance ≥50% improvement
- ✅ Zero N+1 queries (validated)
- ✅ Soft delete pattern applied
- ✅ Audit fields included
- ✅ 100% schema correctness

---

## HANDOFFS

- **To @api-dev:** If new model requires API endpoints ("Create CRUD endpoints for Invoice")
- **To @ai-arch:** If model stores AI results ("Add structured output field for crew results")

---

## ACCEPTANCE CHECKLIST

- [ ] Model defined with all core fields
- [ ] Foreign keys set with cascade semantics
- [ ] Relationships include back_populates
- [ ] Indexes created for performance queries
- [ ] Soft delete applied (deleted_at field)
- [ ] Audit fields included (created_at, updated_at, deleted_at)
- [ ] Migration prepared (Alembic)
- [ ] No N+1 queries in common patterns
- [ ] Query tests show ≥50% improvement
- [ ] Cross-module dependencies documented

**Version:** 1.0 | Last Updated: 2026-05-07
