person_value_batches = [
    "('Alice', 'painting', 34),('Bob', 'cycling', 29),('Cathy', 'photography', 25),('David', 'hiking', 32)",
    "('Eva', 'reading', 28),('Frank', 'cooking', 31),('Grace', 'gardening', 40),('Henry', 'swimming', 22),('Ivy', 'dancing', 26)",
    "('Jack', 'fishing', 35),('Karen', 'knitting', 37),('Leo', 'running', 30),('Mona', 'yoga', 33),('Nate', 'gaming', 24),('Olivia', 'traveling', 27)",
    "('Paul', 'writing', 29),('Quincy', 'woodworking', 38),('Rachel', 'bird watching', 41),('Sam', 'tennis', 23),('Tina', 'surfing', 36),('Uma', 'scuba diving', 34),('Victor', 'guitar', 29),('Wendy', 'baking', 25),('Xander', 'archery', 32),('Yara', 'singing', 28),('Zane', 'skiing', 31),('Amy', 'pottery', 40),('Brian', 'rock climbing', 22),('Cara', 'chess', 26),('Derek', 'camping', 35),('Ella', 'scrapbooking', 37)",
    "('Finn', 'kayaking', 30),('Gina', 'horseback riding', 33),('Hank', 'bird watching', 24)",
    "('Iris', 'jogging', 27),('Jake', 'drumming', 29),('Kara', 'quilting', 38),('Liam', 'painting', 41)",
    "('Mia', 'snowboarding', 23),('Noah', 'skateboarding', 36)",
    "('Owen', 'fencing', 34),('Pia', 'calligraphy', 29),('Quinn', 'magic tricks', 25),('Rita', 'ice skating', 32)",
    "('Sean', 'flying drones', 28),('Tara', 'kitesurfing', 31),('Ursula', 'diving', 40),('Vince', 'model building', 22),('Wade', 'metal detecting', 26),('Xena', 'embroidery', 35)",
    "('Yvonne', 'origami', 37),('Zach', 'boxing', 30),('Anna', 'pilates', 33),('Blake', 'geocaching', 24),('Clara', 'bird watching', 27),('Dean', 'puzzle solving', 29),('Eliza', 'knitting', 38),('Frankie', 'watercolor', 41)",
    "('George', 'trampolining', 23),('Holly', 'bowling', 36),('Ian', 'robotics', 34),('Jess', 'blogging', 29),('Kurt', 'crossfit', 25),('Lila', 'tattoo art', 32),('Mark', 'poetry', 28),('Nina', 'ceramics', 31),('Oscar', 'dog training', 40),('Penny', 'antiquing', 22),('Quentin', 'spelunking', 26),('Roxy', 'hiking', 35)",
    "('Stan', 'glass blowing', 37),('Tina', 'surfing', 30),('Ulysses', 'blacksmithing', 33),('Vera', 'hula hooping', 24),('Wyatt', 'model trains', 27),('Ximena', 'fencing', 29),('Yosef', 'yoga', 38),('Zoey', 'candle making', 41),('Aria', 'songwriting', 23),('Ben', 'jujitsu', 36),('Cora', 'sailing', 34),('Dylan', 'freediving', 29)",
    "('Eve', 'cheerleading', 25),('Felix', 'marathon running', 32),('Gwen', 'pottery', 28),('Harvey', 'chess', 31),('Ivy', 'dancing', 40),('John', 'reading', 22)",
    "('Kelly', 'bird watching', 26),('Landon', 'golfing', 35)",
    "('Mara', 'yoga', 37),('Nate', 'gaming', 30),('Opal', 'puzzles', 33),('Pete', 'skateboarding', 24)",
    "('Quinn', 'quilting', 27),('Rose', 'photography', 29),('Seth', 'sculpting', 38),('Tina', 'surfing', 41),('Uri', 'wood carving', 23)",
    "('Val', 'magic tricks', 36),('Willa', 'writing', 34),('Xavier', 'coding', 29),('Yara', 'singing', 25),('Zane', 'skiing', 32),('Anya', 'painting', 28)",
    "('Blake', 'rock climbing', 31),('Cleo', 'swimming', 40),('Dane', 'running', 22),('Ella', 'gardening', 26),('Finn', 'kayaking', 35),('Gia', 'knitting', 37),('Hugh', 'writing', 30),('Iris', 'jogging', 33),('Jake', 'drumming', 24),('Kara', 'quilting', 27),('Leo', 'running', 29),('Mona', 'yoga', 38),('Nina', 'ceramics', 41),('Owen', 'fencing', 23),('Pia', 'calligraphy', 36),('Quincy', 'magic tricks', 34),('Rita', 'ice skating', 29)",
    "('Sean', 'flying drones', 25),('Tara', 'kitesurfing', 32),('Ursula', 'diving', 28),('Victor', 'guitar', 31),('Wendy', 'baking', 40),('Xander', 'archery', 22),('Yvonne', 'origami', 26),('Zach', 'boxing', 35),('Amy', 'pottery', 37),('Brian', 'rock climbing', 30),('Cara', 'chess', 33)",
    "('Derek', 'camping', 24),('Eva', 'reading', 27),('Frank', 'cooking', 29),('Grace', 'gardening', 38),('Henry', 'swimming', 41),('Ivy', 'dancing', 23),('Jack', 'fishing', 36),('Karen', 'knitting', 34),('Leo', 'running', 29),('Mona', 'yoga', 25),('Nate', 'gaming', 32),('Olivia', 'traveling', 28),('Paul', 'writing', 31),('Quincy', 'woodworking', 40)",
    "('Rachel', 'bird watching', 22),('Sam', 'tennis', 26),('Tina', 'surfing', 35),('Uma', 'scuba diving', 37),('Victor', 'guitar', 30),('Wendy', 'baking', 33),('Xander', 'archery', 24),('Yara', 'singing', 27)",
    "('Zane', 'skiing', 29),('Alice', 'painting', 38),('Bob', 'cycling', 41),('Cathy', 'photography', 23),('David', 'hiking', 36),('Eva', 'reading', 34),('Frank', 'cooking', 29),('Grace', 'gardening', 25),('Henry', 'swimming', 32),('Ivy', 'dancing', 28),('Jack', 'fishing', 31),('Karen', 'knitting', 40),('Leo', 'running', 22),('Mona', 'yoga', 26),('Nate', 'gaming', 35)",
    "('Olivia', 'traveling', 37),('Paul', 'writing', 30),('Quincy', 'woodworking', 33),('Rachel', 'bird watching', 24),('Sam', 'tennis', 27),('Tina', 'surfing', 29),('Uma', 'scuba diving', 38),('Victor', 'guitar', 41),('Wendy', 'baking', 23),('Xander', 'archery', 36)",
    "('Yara', 'singing', 34),('Zane', 'skiing', 29),('Amy', 'pottery', 25),('Brian', 'rock climbing', 32),('Cara', 'chess', 28),('Derek', 'camping', 31),('Eva', 'reading', 40),('Frank', 'cooking', 22),('Grace', 'gardening', 26),('Henry', 'swimming', 35),('Ivy', 'dancing', 37),('Jack', 'fishing', 30),('Karen', 'knitting', 33)",
    "('Leo', 'running', 24),('Mona', 'yoga', 27),('Nate', 'gaming', 29),('Olivia', 'traveling', 38),('Paul', 'writing', 41),('Quincy', 'woodworking', 23),('Rachel', 'bird watching', 36),('Sam', 'tennis', 34),('Tina', 'surfing', 29),('Uma', 'scuba diving', 25),('Victor', 'guitar', 32),('Wendy', 'baking', 28),('Xander', 'archery', 31)",
    "('Yara', 'singing', 40),('Zane', 'skiing', 22),('Alice', 'painting', 26),('Bob', 'cycling', 35),('Cathy', 'photography', 37),('David', 'hiking', 30),('Eva', 'reading', 33),('Frank', 'cooking', 24)",
    "('Grace', 'gardening', 27),('Henry', 'swimming', 29),('Ivy', 'dancing', 38),('Jack', 'fishing', 41),('Karen', 'knitting', 23),('Leo', 'running', 36),('Mona', 'yoga', 34),('Nate', 'gaming', 29),('Olivia', 'traveling', 25),('Paul', 'writing', 32),('Quincy', 'woodworking', 28),('Rachel', 'bird watching', 31),('Sam', 'tennis', 40),('Tina', 'surfing', 22)"
]

position_value_batches = [
    "(1, 'manager', 'Oversees daily operations and ensures efficiency'),(2, 'developer', 'Creates and maintains software applications'),(3, 'analyst', 'Analyzes data and generates reports for decision-making'),(4, 'designer', 'Develops visual concepts for digital and print media'),(5, 'tester', 'Tests software to ensure functionality and performance'),(6, 'administrator', 'Manages IT infrastructure and systems')",
    "(7, 'engineer', 'Designs and develops engineering solutions'),(8, 'consultant', 'Provides expert advice to improve business processes'),(9, 'technician', 'Performs technical support and maintenance tasks'),(10, 'coordinator', 'Organizes and coordinates project activities'),(11, 'specialist', 'Focuses on specific areas within a field or industry'),(12, 'architect', 'Designs system and software architectures'),(13, 'planner', 'Plans and schedules project timelines and resources')",
    "(14, 'strategist', 'Develops strategies to achieve business goals'),(15, 'executive', 'Makes high-level decisions and manages company operations')",
    "(16, 'officer', 'Enforces rules and ensures compliance'),(17, 'supervisor', 'Supervises and guides team members'),(18, 'trainer', 'Conducts training sessions for employees')",
    "(19, 'auditor', 'Audits financial records and ensures accuracy'),(20, 'accountant', 'Manages financial accounts and transactions')",
    "(21, 'recruiter', 'Finds and hires qualified candidates for job openings'),(22, 'marketer', 'Develops and implements marketing campaigns'),(23, 'editor', 'Edits and proofreads content for accuracy and quality'),(24, 'writer', 'Writes content for various platforms and publications'),(25, 'producer', 'Produces multimedia content for distribution'),(26, 'director', 'Directs and oversees department activities'),(27, 'broker', 'Facilitates transactions between buyers and sellers'),(28, 'agent', 'Represents clients in negotiations and transactions')",
    "(29, 'researcher', 'Conducts research to gather information and insights'),(30, 'investigator', 'Investigates issues and gathers evidence'),(31, 'librarian', 'Manages library resources and assists patrons')",
    "(32, 'curator', 'Manages collections in museums or galleries'),(33, 'scientist', 'Conducts scientific research and experiments'),(34, 'biologist', 'Studies living organisms and their environments'),(35, 'chemist', 'Studies chemical substances and reactions'),(36, 'physicist', 'Studies physical properties and laws of nature')",
    "(37, 'geologist', 'Studies the earth and its composition'),(38, 'economist', 'Analyzes economic data and trends'),(39, 'sociologist', 'Studies social behavior and societies'),(40, 'psychologist', 'Studies mental processes and behavior'),(41, 'therapist', 'Provides therapy to improve mental health'),(42, 'counselor', 'Provides guidance and support to clients'),(43, 'nurse', 'Provides medical care to patients'),(44, 'doctor', 'Diagnoses and treats illnesses'),(45, 'pharmacist', 'Dispenses medications and provides advice on their use'),(46, 'surgeon', 'Performs surgical procedures'),(47, 'dentist', 'Provides dental care and treatment')",
    "(48, 'veterinarian', 'Provides medical care to animals'),(49, 'teacher', 'Educates students in various subjects'),(50, 'professor', 'Teaches and conducts research at a university'),(51, 'principal', 'Manages school operations and staff'),(52, 'coach', 'Trains and guides athletes or teams'),(53, 'artist', 'Creates visual art and works of creativity'),(54, 'musician', 'Performs and composes music')",
    "(55, 'actor', 'Performs in theatrical productions and films'),(56, 'director', 'Directs theatrical productions and films'),(57, 'producer', 'Produces films, TV shows, or music'),(58, 'dancer', 'Performs dance routines and choreography')",
    "(59, 'choreographer', 'Creates and directs dance routines'),(60, 'photographer', 'Takes and edits photographs'),(61, 'videographer', 'Records and edits video footage'),(62, 'journalist', 'Reports news and writes articles'),(63, 'reporter', 'Investigates and reports on news stories'),(64, 'editor', 'Reviews and edits written content')",
    "(65, 'publisher', 'Oversees the production and distribution of publications'),(66, 'publicist', 'Manages public relations and media communications'),(67, 'spokesperson', 'Represents an organization in public communications'),(68, 'diplomat', 'Represents a country in foreign affairs'),(69, 'ambassador', 'Acts as a representative in diplomatic matters'),(70, 'politician', 'Engages in political activities and holds public office'),(71, 'legislator', 'Makes laws and policies'),(72, 'judge', 'Presides over legal proceedings and makes rulings'),(73, 'lawyer', 'Provides legal advice and represents clients'),(74, 'paralegal', 'Assists lawyers with legal tasks'),(75, 'mediator', 'Facilitates negotiation and conflict resolution'),(76, 'consultant', 'Provides expert advice to organizations'),(77, 'advisor', 'Offers advice and guidance on various matters'),(78, 'mentor', 'Guides and supports less experienced individuals'),(79, 'coach', 'Trains and develops skills in individuals or teams'),(80, 'instructor', 'Teaches specific skills or subjects')",
    "(81, 'tutor', 'Provides individualized academic assistance'),(82, 'lecturer', 'Gives educational talks and presentations'),(83, 'author', 'Writes books and other written works'),(84, 'blogger', 'Writes and manages a blog'),(85, 'influencer', 'Uses social media to influence and engage with audiences'),(86, 'podcaster', 'Creates and hosts podcasts'),(87, 'youtuber', 'Creates and uploads videos on YouTube'),(88, 'streamer', 'Streams live content on platforms like Twitch'),(89, 'gamer', 'Plays video games professionally or as a hobby')",
    "(90, 'reviewer', 'Reviews products, services, or media'),(91, 'critic', 'Evaluates and critiques creative works'),(92, 'moderator', 'Oversees online forums and discussions'),(93, 'administrator', 'Manages administrative tasks and operations'),(94, 'clerk', 'Performs clerical and administrative duties')",
    "(95, 'assistant', 'Provides support and assistance to others'),(96, 'secretary', 'Manages office tasks and schedules'),(97, 'receptionist', 'Greets visitors and manages front desk duties'),(98, 'cashier', 'Handles cash transactions and customer service'),(99, 'salesperson', 'Sells products or services to customers'),(100, 'customer service representative', 'Provides assistance and support to customers')",
]

import yaml

from sql_engine.engine import DatabaseEngine
from sql_engine.config.config import Config

if __name__ == '__main__':
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        engine = DatabaseEngine(config)
    
    while True:
        try:
            s = input('sql_command > ')
        except EOFError:
            break
        if not s: 
            continue


        if s == 'load':
            for batch in person_value_batches:
                statement = f'insert into persons (name, hobby, age) values {batch}'
                engine.process_command(statement)
            for batch in position_value_batches:
                statement = f'insert into positions (id, name, description) values {batch}'
                engine.process_command(statement)
        else:
            engine.process_command(s)