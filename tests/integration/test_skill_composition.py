"""Integration tests for skills working together."""

import pytest
from skills import BrainstormingSkill, DomainModelingSkill
from domain import ConceptType, IdeaStatus


class TestBrainstormingAndDomainModeling:
    """Test how brainstorming and domain modeling skills work together."""
    
    def test_brainstorm_ideas_become_domain_concepts(self):
        """
        Integration: Brainstorm ideas can be converted to domain concepts.
        
        Workflow:
        1. Brainstorm multiple architecture ideas
        2. Select the best one
        3. Model that architecture in domain model
        """
        # Step 1: Brainstorm architecture approaches
        brainstorm_skill = BrainstormingSkill()
        session = brainstorm_skill.create_session(
            "How should we structure the auth system?"
        )
        
        idea1 = brainstorm_skill.add_idea(
            session,
            title="Monolithic Auth",
            description="Single auth service handling all operations"
        )
        
        idea2 = brainstorm_skill.add_idea(
            session,
            title="Microservices Auth",
            description="Separate services for different auth aspects"
        )
        
        # Step 2: Select the best approach
        session.select_idea(idea1)
        outcome = brainstorm_skill.select_best_idea(session)
        
        assert outcome.selected_title == "Monolithic Auth"
        assert idea1.status == IdeaStatus.SELECTED
        
        # Step 3: Model the selected architecture
        domain_skill = DomainModelingSkill()
        model = domain_skill.create_model(
            "Auth System",
            f"Architecture: {outcome.selected_title}"
        )
        
        # Add core concepts from the architecture
        domain_skill.add_concept(
            model,
            "User",
            "An entity representing a system user",
            ConceptType.ENTITY,
            examples=["Admin", "Regular User"]
        )
        
        domain_skill.add_concept(
            model,
            "AuthToken",
            "A value object representing authentication proof",
            ConceptType.VALUE_OBJECT,
            examples=["JWT Token", "Session Token"],
            invariants=["Must be cryptographically secure"]
        )
        
        domain_skill.add_concept(
            model,
            "AuthService",
            "The service responsible for authentication",
            ConceptType.SERVICE
        )
        
        # Verify the model
        validation = domain_skill.validate_model(model)
        assert validation["is_valid"] is True
        assert validation["concept_count"] == 3
        
        # Generate summary
        summary = domain_skill.generate_summary(model)
        assert "Auth System" in summary
        assert "User" in summary
        assert "AuthToken" in summary
        assert "AuthService" in summary
    
    def test_brainstorm_multiple_domain_approaches(self):
        """
        Integration: Brainstorm multiple domain modeling approaches.
        
        Workflow:
        1. Brainstorm different domain modeling strategies
        2. For each idea, create a domain model
        3. Compare models
        """
        brainstorm_skill = BrainstormingSkill()
        domain_skill = DomainModelingSkill()
        
        session = brainstorm_skill.create_session(
            "How should we model the payment domain?"
        )
        
        ideas = [
            ("Transaction-Focused", "Model centered on payment transactions"),
            ("Account-Focused", "Model centered on user accounts and balances"),
            ("Event-Sourced", "Model based on immutable payment events")
        ]
        
        models = {}
        
        # Create a model for each idea
        for idea_title, idea_desc in ideas:
            idea = brainstorm_skill.add_idea(session, idea_title, idea_desc)
            
            model = domain_skill.create_model(
                f"Payment Domain: {idea_title}",
                idea_desc
            )
            
            # Add concepts based on the approach
            if "Transaction" in idea_title:
                domain_skill.add_concept(
                    model,
                    "Payment",
                    "A single payment transaction",
                    ConceptType.ENTITY
                )
                domain_skill.add_concept(
                    model,
                    "TransactionLog",
                    "Record of all transactions",
                    ConceptType.AGGREGATE
                )
            
            elif "Account" in idea_title:
                domain_skill.add_concept(
                    model,
                    "Account",
                    "User account with balance",
                    ConceptType.AGGREGATE
                )
                domain_skill.add_concept(
                    model,
                    "Balance",
                    "Account balance value",
                    ConceptType.VALUE_OBJECT
                )
            
            elif "Event" in idea_title:
                domain_skill.add_concept(
                    model,
                    "PaymentEvent",
                    "Immutable payment event",
                    ConceptType.EVENT
                )
                domain_skill.add_concept(
                    model,
                    "EventStore",
                    "Repository for payment events",
                    ConceptType.REPOSITORY
                )
            
            models[idea_title] = model
        
        # Verify all models are valid
        for title, model in models.items():
            validation = domain_skill.validate_model(model)
            assert validation["is_valid"] is True, f"{title} failed validation"
        
        # Select the best approach
        session.select_idea(session.ideas[0])
        # (Just verify all models were created successfully)
        assert len(models) == 3
        
        # Generate summaries for comparison
        summaries = {
            title: domain_skill.generate_summary(model)
            for title, model in models.items()
        }
        
        assert "Transaction-Focused" in summaries
        assert "Account-Focused" in summaries
        assert "Event-Sourced" in summaries
    
    def test_skill_composition_workflow(self):
        """
        Integration: Full workflow using both skills in sequence.
        
        This demonstrates how skills can be chained together:
        1. Brainstorm feature ideas
        2. Brainstorm domain modeling approaches
        3. Create the domain model
        4. Add concepts to the model
        """
        brainstorm_skill = BrainstormingSkill()
        domain_skill = DomainModelingSkill()
        
        # Phase 1: Brainstorm features
        feature_session = brainstorm_skill.create_session(
            "What features should the CLI have?"
        )
        
        brainstorm_skill.add_idea(
            feature_session,
            "Interactive Setup",
            "Guide users through configuration"
        )
        
        brainstorm_skill.add_idea(
            feature_session,
            "Command-Line Interface",
            "Direct CLI commands for automation"
        )
        
        feature_session.select_idea(feature_session.ideas[0])
        
        # Phase 2: Brainstorm architecture
        arch_session = brainstorm_skill.create_session(
            "How should we architect the CLI?"
        )
        
        monolith = brainstorm_skill.add_idea(
            arch_session,
            "Single Module",
            "All CLI logic in one module"
        )
        
        modular = brainstorm_skill.add_idea(
            arch_session,
            "Modular Design",
            "Separate modules for each command"
        )
        
        arch_session.select_idea(modular)
        
        # Phase 3: Create domain model
        model = domain_skill.create_model(
            "CLI Architecture",
            "Modular CLI with separate command modules"
        )
        
        # Add concepts
        domain_skill.add_concept(
            model,
            "Command",
            "A CLI command that can be executed",
            ConceptType.AGGREGATE
        )
        
        domain_skill.add_concept(
            model,
            "Parameter",
            "Input parameter for a command",
            ConceptType.VALUE_OBJECT
        )
        
        domain_skill.add_concept(
            model,
            "Result",
            "Output from executing a command",
            ConceptType.VALUE_OBJECT
        )
        
        # Verify the complete workflow
        assert feature_session.selected_idea is not None
        assert arch_session.selected_idea == modular
        validation = domain_skill.validate_model(model)
        assert validation["is_valid"] is True
        assert validation["concept_count"] == 3
