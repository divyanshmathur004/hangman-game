import random
import string
import time

DIFFICULTY_CONFIG = {
    "Easy": {"max_wrong": 8, "base_score": 80, "time_limit": 0, "min_len": 3, "max_len": 5},
    "Medium": {"max_wrong": 6, "base_score": 120, "time_limit": 60, "min_len": 5, "max_len": 8},
    "Hard": {"max_wrong": 5, "ba se_score": 170, "time_limit": 40, "min_len": 7, "max_len": 99},
}

HINT_COSTS = [0, 1, 2]

WORD_BANK = [
    # Animals - Easy
    {"word": "cat", "category": "Animals", "difficulty": "Easy", "hints": ["Pet animal", "Says meow", "3 letters"]},
    {"word": "dog", "category": "Animals", "difficulty": "Easy", "hints": ["Man's best friend", "Barks", "3 letters"]},
    {"word": "lion", "category": "Animals", "difficulty": "Easy", "hints": ["King of jungle", "Big cat", "Has a mane"]},
    {"word": "tiger", "category": "Animals", "difficulty": "Easy", "hints": ["Striped big cat", "Carnivore", "Orange fur"]},
    {"word": "zebra", "category": "Animals", "difficulty": "Easy", "hints": ["Striped animal", "Looks like horse", "Black and white"]},
    {"word": "rabbit", "category": "Animals", "difficulty": "Easy", "hints": ["Long ears", "Eats carrots", "Hops"]},
    {"word": "monkey", "category": "Animals", "difficulty": "Easy", "hints": ["Climbs trees", "Likes bananas", "Very playful"]},
    {"word": "panda", "category": "Animals", "difficulty": "Easy", "hints": ["Black and white bear", "Eats bamboo", "From China"]},

    # Animals - Medium
    {"word": "giraffe", "category": "Animals", "difficulty": "Medium", "hints": ["Tallest animal", "Long neck", "Spotted body"]},
    {"word": "elephant", "category": "Animals", "difficulty": "Medium", "hints": ["Largest land animal", "Has trunk", "Big ears"]},
    {"word": "kangaroo", "category": "Animals", "difficulty": "Medium", "hints": ["From Australia", "Jumps", "Carries baby in pouch"]},
    {"word": "dolphin", "category": "Animals", "difficulty": "Medium", "hints": ["Very intelligent", "Lives in ocean", "Makes clicking sounds"]},

    # Space - Easy
    {"word": "star", "category": "Space", "difficulty": "Easy", "hints": ["Shines at night", "Sun is one", "Seen in sky"]},
    {"word": "moon", "category": "Space", "difficulty": "Easy", "hints": ["Earth's satellite", "Glows at night", "Changes shape"]},
    {"word": "planet", "category": "Space", "difficulty": "Easy", "hints": ["Orbits a star", "Earth is one", "In solar system"]},

    # Space - Medium
    {"word": "galaxy", "category": "Space", "difficulty": "Medium", "hints": ["Milky Way is one", "Contains stars", "Very large system"]},
    {"word": "asteroid", "category": "Space", "difficulty": "Medium", "hints": ["Space rock", "Orbits sun", "Found in belt"]},
    {"word": "comet", "category": "Space", "difficulty": "Medium", "hints": ["Has tail", "Ice and dust", "Seen in sky rarely"]},
    {"word": "satellite", "category": "Space", "difficulty": "Medium", "hints": ["Orbits planet", "Used for communication", "Artificial ones exist"]},

    # Space - Hard
    {"word": "supernova", "category": "Space", "difficulty": "Hard", "hints": ["Exploding star", "Very bright", "Astronomy event"]},
    {"word": "constellation", "category": "Space", "difficulty": "Hard", "hints": ["Group of stars", "Forms patterns", "Seen in night sky"]},

    # Programming - Easy
    {"word": "python", "category": "Programming", "difficulty": "Easy", "hints": ["Programming language", "Also a snake", "Popular for AI"]},
    {"word": "java", "category": "Programming", "difficulty": "Easy", "hints": ["Programming language", "Used for Android", "Coffee nickname"]},
    {"word": "html", "category": "Programming", "difficulty": "Easy", "hints": ["Markup language", "Used for websites", "Defines structure"]},
    {"word": "code", "category": "Programming", "difficulty": "Easy", "hints": ["Written by developers", "Used to build software", "Programming task"]},

    # Programming - Medium
    {"word": "variable", "category": "Programming", "difficulty": "Medium", "hints": ["Stores value", "Used in coding", "Name and data"]},
    {"word": "function", "category": "Programming", "difficulty": "Medium", "hints": ["Reusable code", "Performs task", "Called in program"]},
    {"word": "loop", "category": "Programming", "difficulty": "Medium", "hints": ["Repeats code", "For and while", "Iteration"]},
    {"word": "compiler", "category": "Programming", "difficulty": "Medium", "hints": ["Translates code", "Machine language", "Build step"]},

    # Programming - Hard
    {"word": "streamlit", "category": "Programming", "difficulty": "Hard", "hints": ["Python web app framework", "Used for dashboards", "Data apps"]},
    {"word": "polymorphism", "category": "Programming", "difficulty": "Hard", "hints": ["OOP concept", "Many forms", "Used in classes"]},
    {"word": "recursion", "category": "Programming", "difficulty": "Hard", "hints": ["Function calling itself", "Algorithm technique", "Divide problem"]},

    # Food - Easy
    {"word": "pizza", "category": "Food", "difficulty": "Easy", "hints": ["Italian dish", "Cheese topping", "Round"]},
    {"word": "burger", "category": "Food", "difficulty": "Easy", "hints": ["Fast food", "Has bun", "Contains patty"]},
    {"word": "apple", "category": "Food", "difficulty": "Easy", "hints": ["Fruit", "Keeps doctor away", "Red or green"]},
    {"word": "mango", "category": "Food", "difficulty": "Easy", "hints": ["King of fruits", "Sweet", "Yellow"]},

    # Food - Medium
    {"word": "pancake", "category": "Food", "difficulty": "Medium", "hints": ["Breakfast food", "Flat and round", "Served with syrup"]},
    {"word": "spaghetti", "category": "Food", "difficulty": "Medium", "hints": ["Italian pasta", "Long noodles", "Served with sauce"]},

    # Technology - Medium
    {"word": "internet", "category": "Technology", "difficulty": "Medium", "hints": ["Global network", "Used daily", "Connects computers"]},
    {"word": "browser", "category": "Technology", "difficulty": "Medium", "hints": ["Used to access websites", "Chrome is one", "Surf internet"]},

    # Technology - Hard
    {"word": "encryption", "category": "Technology", "difficulty": "Hard", "hints": ["Secures data", "Used in cybersecurity", "Scrambles information"]},
    {"word": "blockchain", "category": "Technology", "difficulty": "Hard", "hints": ["Crypto technology", "Decentralized", "Ledger system"]},
]


def get_categories() -> list[str]:
    return ["All"] + sorted({w["category"] for w in WORD_BANK})


def _filtered_words(difficulty: str, category: str, used_words: set[str] | None = None) -> list[dict]:
    cfg = DIFFICULTY_CONFIG[difficulty]
    words = [
        w for w in WORD_BANK
        if w["difficulty"] == difficulty and cfg["min_len"] <= len(w["word"]) <= cfg["max_len"]
    ]
    if category != "All":
        words = [w for w in words if w["category"] == category]
    if used_words:
        words = [w for w in words if w["word"] not in used_words]
    return words


def new_game(difficulty: str = "Medium", category: str = "All", used_words: set[str] | None = None) -> dict:
    pool = _filtered_words(difficulty, category, used_words)

    if not pool:
        if used_words is not None:
            used_words.clear()
        pool = _filtered_words(difficulty, category)

    chosen = random.choice(pool)

    if used_words is not None:
        used_words.add(chosen["word"])

    cfg = DIFFICULTY_CONFIG[difficulty]
    return {
        "word": chosen["word"].lower(),
        "category": chosen["category"],
        "difficulty": difficulty,
        "hints": chosen["hints"],
        "hint_level": 0,
        "revealed_hints": 1,
        "correct_letters": set(),
        "wrong_letters": set(),
        "attempts_used": 0,
        "max_wrong": cfg["max_wrong"],
        "time_limit": cfg["time_limit"],
        "start_time": time.time(),
        "game_over": False,
        "won": False,
        "last_event": "start",
        "score_applied": False,
    }


def masked_word(word: str, correct_letters: set[str]) -> str:
    return " ".join(ch if ch in correct_letters else "_" for ch in word)


def attempts_left(state: dict) -> int:
    return max(0, state["max_wrong"] - state["attempts_used"])


def current_hints(state: dict) -> list[str]:
    return state["hints"][:state["revealed_hints"]]


def reveal_next_hint(state: dict) -> dict:
    if state["game_over"]:
        return state

    if state["revealed_hints"] >= len(state["hints"]):
        return state

    next_index = state["revealed_hints"]
    cost = HINT_COSTS[min(next_index, len(HINT_COSTS) - 1)]
    state["revealed_hints"] += 1
    state["hint_level"] = state["revealed_hints"] - 1
    state["attempts_used"] += cost
    state["last_event"] = "hint"

    if state["attempts_used"] >= state["max_wrong"]:
        state["game_over"] = True
        state["won"] = False
        state["last_event"] = "lost"

    return state


def time_left(state: dict) -> int | None:
    if state["time_limit"] <= 0:
        return None
    remaining = int(state["time_limit"] - (time.time() - state["start_time"]))
    return max(0, remaining)


def expire_if_needed(state: dict) -> dict:
    remaining = time_left(state)
    if remaining is not None and remaining <= 0 and not state["game_over"]:
        state["game_over"] = True
        state["won"] = False
        state["last_event"] = "timeout"
    return state


def apply_guess(state: dict, letter: str) -> dict:
    state = expire_if_needed(state)
    if state["game_over"]:
        return state

    letter = letter.lower().strip()
    if len(letter) != 1 or letter not in string.ascii_lowercase:
        state["last_event"] = "invalid"
        return state

    if letter in state["correct_letters"] or letter in state["wrong_letters"]:
        state["last_event"] = "repeat"
        return state

    if letter in state["word"]:
        state["correct_letters"].add(letter)
        state["last_event"] = "correct"
    else:
        state["wrong_letters"].add(letter)
        state["attempts_used"] += 1
        state["last_event"] = "wrong"

    if all(ch in state["correct_letters"] for ch in state["word"]):
        state["game_over"] = True
        state["won"] = True
        state["last_event"] = "won"
    elif state["attempts_used"] >= state["max_wrong"]:
        state["game_over"] = True
        state["won"] = False
        state["last_event"] = "lost"

    return state


MAX_WRONG = DIFFICULTY_CONFIG["Medium"]["max_wrong"]