from datetime import datetime

from db_management.entities_CRUD import score_CRUD, user_CRUD
from db_management.models.entities import Score


async def create_score(user_id: str) -> str:
    user = await user_CRUD.get_user(user_id)
    new_score = Score(
        user_id=user.id,
        total_score=0,
        level=1,
        rank_earned="",
        streak_days=1,
        resource_streak_days=0,
        resources_created=0,
        last_activity_date=datetime(1, 1, 1),
        last_resource_creation_date=datetime(1, 1, 1)
    )
    user.score_id = new_score.id
    return await score_CRUD.create_score(new_score)


async def get_user_score(user_id: str) -> Score:
    return await score_CRUD.get_user_score(user_id)


async def update_score(user_id: str, activity: str) -> bool:
    user_score = await get_user_score(user_id)  # קבלת הניקוד של המשתמש
    additional_score = get_additional_score(activity)
    if datetime.now() != user_score.last_activity_date:  # אם תאריך הפעילות האחרונה שונה מהתאריך הנוכחי
        if get_streak_days(
                user_score.last_activity_date):  # אם תאריך הפעילות האחרונה היה אתמול מעלה את מונה רצף הימים,
            # אחרת מחזיר את המונה ל1
            user_score.streak_days += 1
            additional_score += get_streak_days_score(user_score.streak_days)  # קבלת ניקוד על ימי פעילות רציפים

        else:
            user_score.streak_days = 1
        if activity == "Resource Creation":  # אם הפעילות היא יצירת משאב
            user_score.resources_created += 1  # מעלה את מונה המשאבים
            get_total_resources_created_score(user_score.resources_created)
            if get_resource_streak_days(
                    user_score.last_resource_creation_date):  # תאריך יצירת המשאב האחרון שונה מהתאריך הנוכחי
                user_score.resource_streak_days += 1  # מעלה את מונה רצף יצירת המשאבים
                additional_score += get_resource_streak_score(
                    user_score.resource_streak_days)  # קבלת ניקוד על רצף ימי יצירת משאבים
    user_score.total_score += additional_score  # מוסיף למשתנה את הנקודות
    user_score.level = get_level(user_score.total_score)  # משנה את הדרגה בהתאם לניקוד המעודכן
    user_score.rank = get_rank(user_score.total_score)  # משנה את הראנק בהתאם לניקוד המעודכן
    user_score.last_activity_date = datetime.now()  # מעדכן את תאריך הפעילות האחרונה לתאריך הנוכחי
    score_id = user_score.id
    return await score_CRUD.update_score(score_id, user_score)  # שולח את הID של הניקוד ואת הניקוד המעודכן לעידכון


def get_additional_score(activity: str):
    score_per_activity_dict = {
        "Exercise Completion": 5,
        "Course Participation": 10,
        "Biofeedback Scan": 10,
        "Correct Course Answers": 10,
        "Resource Creation": 5,
        "Challenge Completion": 25
    }
    for key in score_per_activity_dict.keys():
        if key == activity:
            return score_per_activity_dict[key]
    return 0


def get_level(score):
    level_points_dict = {
        1: 10,
        2: 50,
        3: 150,
        4: 250,
        5: 375,
        6: 500,
        7: 650,
        8: 825,
        9: 950,
        10: 1150,
        11: 1350,
        12: 1560,
        13: 1800,
        14: 2100,
        15: 2500,
        16: 2950,
        17: 3430,
        18: 3940,
        19: 4480,
        20: 5050,
        21: 5650,
        22: 6280,
        23: 6940,
        24: 7630,
        25: 8350,
        26: 9100,
        27: 9880,
        28: 10690,
        29: 11530,
        30: 12400
    }

    for threshold, status in sorted(level_points_dict.items(), reverse=True):
        if score >= threshold:
            return status

    return list(level_points_dict.values())[-1]


def get_rank(score):
    points_rank_dict = {
        10: 'Eagle Apprentice',
        250: 'Horse Practitioner',
        650: 'Elephant Zen',
        1150: 'Elephant Guru',
        1800: 'Dolphin Sensei',
        3940: 'Bear Guru',
        6940: 'Rhino Legend',
        10690: 'Rhino Master',
    }

    for threshold, status in sorted(points_rank_dict.items(), reverse=True):
        if score >= threshold:
            return status

    return list(points_rank_dict.values())[-1]


def get_streak_days(last_activity_date: datetime):  # מחזיר האם הימים רצופים
    current_date = datetime.now()
    if (current_date - last_activity_date).days == 1:
        return 1  # the streak was stopped
    else:
        return 0


def get_resource_streak_days(last_resource_creation_date: datetime):  # מחזיר האם ימי יצירת המשאבים רצופים
    current_date = datetime.now()
    if (current_date - last_resource_creation_date).days == 1:
        return 1  # the streak was stopped
    else:
        return 0


def get_streak_days_score(streak_days: int):  # מחזיר את הניקוד על רצף ימי פעילות
    streak_days_score_dict = {
        3: 30,
        5: 50,
        10: 100,
        15: 120,
        20: 140,
        30: 170,
        45: 220,
        60: 270,
        90: 400,
        100: 550
    }
    for key in streak_days_score_dict.keys():
        if key == streak_days:
            return streak_days_score_dict[key]
    return 0


def get_resource_streak_score(resource_creation_streak: int):  # מחזיר את הניקוד על רצף יצירת משאבים
    resource_creation_streak_dict = {
        3: 30,
        5: 50,
        10: 100,
        20: 250
    }
    for key in resource_creation_streak_dict.keys():
        if key == resource_creation_streak:
            return resource_creation_streak_dict[key]
    return 0


def get_total_resources_created_score(resources_created):  # מחזיר את הניקוד של יצירת משאבים
    total_resources_created_dict = {
        5: 60,
        10: 100,
        200: 200,
        300: 300
    }
    for key in total_resources_created_dict.keys():
        if key == resources_created:
            return total_resources_created_dict[key]
    return 0
