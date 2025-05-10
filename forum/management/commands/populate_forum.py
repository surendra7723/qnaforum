import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from faker import Faker
from forum.models import (
    UserProfile, Question, Answer, QuestionVote, AnswerVote, Report
)

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with dummy forum data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--questions', type=int, default=30, help='Number of questions to create')
        parser.add_argument('--answers', type=int, default=100, help='Number of answers to create')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before populating')

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        num_users = options['users']
        num_questions = options['questions']
        num_answers = options['answers']

        # Create users and profiles
        users = self.create_users(num_users)
        if not users:
            self.stdout.write(self.style.ERROR('Failed to create users. Aborting.'))
            return
        self.stdout.write(self.style.SUCCESS(f'Created/found {len(users)} users'))

        # Create questions
        questions = self.create_questions(users, num_questions)
        if not questions:
            self.stdout.write(self.style.ERROR('Failed to create questions. Aborting.'))
            return
        self.stdout.write(self.style.SUCCESS(f'Created {len(questions)} questions'))

        # Create answers
        answers = self.create_answers(users, questions, num_answers)
        if not answers:
            self.stdout.write(self.style.WARNING('No answers created.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Created {len(answers)} answers'))

            # Create votes for answers
            self.create_answer_votes(users, answers)
            self.stdout.write(self.style.SUCCESS('Created answer votes'))

        # Create votes for questions
        self.create_question_votes(users, questions)
        self.stdout.write(self.style.SUCCESS('Created question votes'))

        # Create reports
        self.create_reports(users, questions)
        self.stdout.write(self.style.SUCCESS('Created reports'))

    def clear_data(self):
        try:
            Report.objects.all().delete()
            self.stdout.write("Cleared reports")
            AnswerVote.objects.all().delete()
            self.stdout.write("Cleared answer votes")
            QuestionVote.objects.all().delete()
            self.stdout.write("Cleared question votes")
            Answer.objects.all().delete()
            self.stdout.write("Cleared answers")
            Question.objects.all().delete()
            self.stdout.write("Cleared questions")
            
            # Only delete user profiles for non-superusers
            UserProfile.objects.filter(user__is_superuser=False).delete()
            self.stdout.write("Cleared user profiles")
            
            # Only delete non-superusers
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write("Cleared non-superuser accounts")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during data clearing: {e}"))

    def create_users(self, count):
        users = []
        # Keep existing users
        try:
            existing_users = list(User.objects.all())
            if existing_users:
                users.extend(existing_users)
                count = max(0, count - len(existing_users))
                
            # Create new users if needed
            for i in range(count):
                username = f"{fake.user_name()}{random.randint(1, 9999)}"
                # Ensure unique username
                while User.objects.filter(username=username).exists():
                    username = f"{fake.user_name()}{random.randint(1, 9999)}"
                    
                email = fake.email()
                password = 'password123'  # Simple password for testing
                
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=fake.first_name(),
                        last_name=fake.last_name()
                    )
                    
                    # Create user profile
                    is_admin = random.choice([True, False, False, False])  # 25% chance of admin
                    if is_admin:
                        user.is_staff = True
                        user.save()
                        UserProfile.objects.create(user=user, role="ADMIN")
                    else:
                        UserProfile.objects.create(user=user, role="USER")
                        
                    users.append(user)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error creating user {username}: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in user creation: {e}"))
            
        return users

    def create_questions(self, users, count):
        if not users:
            return []
            
        questions = []
        try:
            topics = [choice[0] for choice in Question.TOPIC_CHOICES]
            statuses = [choice[0] for choice in Question.STATUS_CHOICES]
            
            # Common question templates by topic
            topic_templates = {
                "GENERAL": [
                    "How does {item} work?",
                    "What are the benefits of {item}?",
                    "When should we use {item}?",
                    "Can someone explain {item}?",
                ],
                "TECHNICAL": [
                    "Best practices for implementing {item}",
                    "How to troubleshoot {item} issues",
                    "Is {item} compatible with {other_item}?",
                    "Optimal configuration for {item}",
                ],
                "FINANCE": [
                    "Budget planning for {item}",
                    "Cost analysis of {item}",
                    "ROI calculation for {item}",
                    "Financial implications of {item}",
                ],
                "HR": [
                    "Hiring process for {item} specialists",
                    "Training requirements for {item}",
                    "Employee feedback on {item}",
                    "Team structure for {item} projects",
                ],
                "FEEDBACK": [
                    "Feedback needed on {item}",
                    "What do you think about {item}?",
                    "How can we improve {item}?",
                    "Suggestions for {item} enhancement",
                ],
                "SALES": [
                    "Selling strategy for {item}",
                    "Customer response to {item}",
                    "Market trends for {item}",
                    "Competitive analysis of {item}",
                ],
                "CUSTOMER": [
                    "Customer satisfaction with {item}",
                    "Common complaints about {item}",
                    "How to improve customer experience with {item}",
                    "Customer retention strategies for {item}",
                ],
            }
            
            # Items to fill in templates
            items = [
                "our new product", "the company policy", "remote work", "team collaboration",
                "project management", "customer support", "marketing strategy", "sales approach",
                "employee onboarding", "performance reviews", "technical documentation",
                "quality assurance", "customer feedback", "market research", "data security",
                "cloud infrastructure", "API integration", "mobile app", "web platform",
                "social media presence", "email campaigns", "content strategy"
            ]
            
            other_items = [
                "existing systems", "third-party tools", "our workflow", "customer expectations",
                "industry standards", "regulatory requirements", "budget constraints",
                "team capabilities", "current infrastructure", "future roadmap"
            ]
            
            for _ in range(count):
                topic = random.choice(topics)
                template = random.choice(topic_templates.get(topic, topic_templates["GENERAL"]))
                item = random.choice(items)
                other_item = random.choice(other_items)
                
                title = template.format(item=item, other_item=other_item)
                if len(title) > 60:
                    title = title[:57] + "..."
                
                content = fake.paragraphs(nb=random.randint(1, 3))
                content = "\n\n".join(content)
                
                created_days_ago = random.randint(0, 120)
                created_at = timezone.now() - timedelta(days=created_days_ago)
                
                status = random.choice(statuses)
                remarks = fake.paragraph() if status != "PENDING" else ""
                
                try:
                    question = Question.objects.create(
                        title=title,
                        content=content,
                        created_by=random.choice(users),
                        created_at=created_at,
                        status=status,
                        remarks=remarks,
                        topic=topic
                    )
                    questions.append(question)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error creating question: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in question creation: {e}"))
            
        return questions

    def create_answers(self, users, questions, count):
        if not users or not questions:
            return []
            
        answers = []
        
        answer_templates = [
            "Based on my experience, {content}",
            "I would suggest {content}",
            "In my opinion, {content}",
            "According to best practices, {content}",
            "The solution is to {content}",
            "We've dealt with this before. {content}",
            "This is actually quite simple: {content}",
            "After analyzing the situation, I believe {content}",
        ]
        
        try:
            for _ in range(count):
                question = random.choice(questions)
                days_after_question = random.randint(0, 30)
                
                # Ensure answer date is after question date
                question_date = question.created_at
                answer_date = question_date + timedelta(days=days_after_question)
                if answer_date > timezone.now():
                    answer_date = timezone.now()
                
                template = random.choice(answer_templates)
                content = template.format(content=fake.paragraph())
                
                # Add additional paragraphs sometimes
                if random.choice([True, False, False]):
                    content += "\n\n" + fake.paragraph()
                    
                # Sometimes add a concluding statement
                if random.choice([True, False]):
                    content += "\n\nHope this helps!"
                
                try:
                    answer = Answer.objects.create(
                        question=question,
                        body=content,
                        answered_by=random.choice(users),
                        answered_at=answer_date,
                        edited=random.choice([True, False, False, False])  # 25% chance of being edited
                    )
                    answers.append(answer)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Error creating answer: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in answer creation: {e}"))
            
        return answers

    def create_question_votes(self, users, questions):
        if not users or not questions:
            return
        
        try:
            # Each user votes on some questions
            for user in users:
                # Vote on 30-70% of questions
                max_votes = min(len(questions), int(len(questions) * 0.7))
                min_votes = min(len(questions), int(len(questions) * 0.3))
                num_to_vote_on = random.randint(min_votes, max_votes)
                
                if num_to_vote_on > 0:
                    questions_to_vote_on = random.sample(questions, num_to_vote_on)
                    
                    for question in questions_to_vote_on:
                        if not QuestionVote.objects.filter(voter=user, question=question).exists():
                            vote_type = random.choice(["LIKE", "DISLIKE", "LIKE", "LIKE"])  # 75% like, 25% dislike
                            try:
                                QuestionVote.objects.create(
                                    question=question,
                                    voter=user,
                                    vote_type=vote_type,
                                    created_at=question.created_at + timedelta(days=random.randint(0, 30))
                                )
                            except IntegrityError:
                                # Skip if there's a uniqueness constraint violation
                                pass
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f"Error creating question vote: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in question vote creation: {e}"))

    def create_answer_votes(self, users, answers):
        if not users or not answers:
            return
            
        try:
            # Each user votes on some answers
            for user in users:
                # Vote on 30-60% of answers
                max_votes = min(len(answers), int(len(answers) * 0.6))
                min_votes = min(len(answers), int(len(answers) * 0.3))
                num_to_vote_on = random.randint(min_votes, max_votes)
                
                if num_to_vote_on > 0:
                    answers_to_vote_on = random.sample(answers, num_to_vote_on)
                    
                    for answer in answers_to_vote_on:
                        if not AnswerVote.objects.filter(voter=user, answer=answer).exists():
                            vote_type = random.choice(["LIKE", "DISLIKE", "LIKE", "LIKE"])  # 75% like, 25% dislike
                            try:
                                AnswerVote.objects.create(
                                    answer=answer,
                                    voter=user,
                                    vote_type=vote_type,
                                    create_at=answer.answered_at + timedelta(days=random.randint(0, 20))
                                )
                            except IntegrityError:
                                # Skip if there's a uniqueness constraint violation
                                pass
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f"Error creating answer vote: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in answer vote creation: {e}"))

    def create_reports(self, users, questions):
        if not users or not questions:
            return
            
        try:
            # About 10% of questions get reported
            num_reports = max(1, int(len(questions) * 0.1))
            num_reports = min(num_reports, len(questions))
            questions_to_report = random.sample(questions, num_reports)
            
            report_feedbacks = [
                "This content is inappropriate.",
                "This question contains misleading information.",
                "This violates community guidelines.",
                "Duplicate of an existing question.",
                "Off-topic or irrelevant.",
                "Contains personal attacks.",
                "Spam content.",
            ]
            
            statuses = [choice[0] for choice in Report.STATUS_CHOICES]
            
            for question in questions_to_report:
                # Ensure we don't try to select more reporters than available users
                num_reporters = min(len(users), random.randint(1, 3))  # 1-3 reports per question
                if num_reporters > 0:
                    reporters = random.sample(users, num_reporters)
                    
                    for user in reporters:
                        status = random.choice(statuses)
                        feedback = random.choice(report_feedbacks)
                        
                        try:
                            Report.objects.create(
                                question=question,
                                feedback=feedback,
                                user=user,
                                status=status,
                                created_at=question.created_at + timedelta(days=random.randint(1, 30)),
                                updated_at=question.created_at + timedelta(days=random.randint(2, 35))
                            )
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"Error creating report: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in report creation: {e}"))