from Database import Database
import math


"""
Note: Delete 'UnderFire.sqlite3' before each run
"""
tests_passed = 0
tests = 0

db = Database()

#################################
# test initial values of tables #
#################################

# test 1
result = db.get_settings()
passed = True
if result["res_height"] != 720:
    passed = False
elif result["res_width"] != 1280:
    passed = False
elif result["difficulty"] != "easy":
    passed = False
elif result["music"] != 50:
    passed = False
elif result["sound"] != 50:
    passed = False

if not passed:
    print("Test 1 failed, initial values for settings table")
    print("Expected values:\nres_height=400, res_width=400, difficulty='easy', music=50, sound=50")
    print("Output:\nres_height=%d, res_width=%d, difficulty=%s, music=%d, sound=%d" %
          (result["res_height"], result["res_width"], result["difficulty"], result["music"], result["sound"]))
else:
    tests_passed += 1
tests += 1

# test 2
result = db.get_stats()
failed_cases = []
for key in result:
    if result[key] != 0:
        failed_cases.append(result[key])
if len(failed_cases) > 0:
    print("Test 2 failed, initial values for stats table")
    print("Expected all 0 values, but got:")
    print(failed_cases)
else:
    tests_passed += 1
tests += 1


# test 3
c4_result = db.get_leaderboard("c4")
etf_result = db.get_leaderboard("etf")
if c4_result is not None or etf_result is not None:
    print("Test 3 failed, None was not returned for an empty leaderboard\nc4_result: ")
    print(c4_result)
    print("etf_result: ")
    print(etf_result)
else:
    tests_passed += 1
tests += 1


# test 4
resultc4 = db.get_game_state("c4")
resultetf = db.get_game_state("etf")
if (resultc4 is not None) or (resultetf is not None):
    print("Test 4 failed, None was not returned when there are no game states")
else:
    tests_passed += 1
tests += 1


#######################
# LeaderBoard Tests #
#######################

# test 5, test addition of a high score to the database
r1 = db.update_leaderboard("c4", "aaa", 50)
r2 = db.update_leaderboard("etf", "aaa", 40)
if r1 != 0 and r2 != 0:
    print("Test 5 failed, function did not return 0 when the insertion should be successful")

c4_result = db.get_leaderboard("c4")
etf_result = db.get_leaderboard("etf")
if c4_result != [("aaa", 50)] or etf_result != [("aaa", 40)]:
    print("Test 5 failed, test addition of a high score to the database")
else:
    tests_passed += 1
tests += 1


# test 6, check if the scores are returned from highest to lowest
db.update_leaderboard("c4", "bbb", 73)
db.update_leaderboard("c4", "ccc", 60)
db.update_leaderboard("c4", "ddd", 70)
db.update_leaderboard("c4", "eee", 80)
db.update_leaderboard("c4", "fff", 90)
db.update_leaderboard("c4", "ggg", 100)
db.update_leaderboard("c4", "hhh", 65)
db.update_leaderboard("c4", "ii6", 52)
db.update_leaderboard("c4", "jjj", 57)

db.update_leaderboard("etf", "bbb", 73)
db.update_leaderboard("etf", "ccc", 60)
db.update_leaderboard("etf", "ddd", 70)
db.update_leaderboard("etf", "eee", 80)
db.update_leaderboard("etf", "fff", 90)
db.update_leaderboard("etf", "ggg", 100)
db.update_leaderboard("etf", "hhh", 65)
db.update_leaderboard("etf", "ii6", 52)
db.update_leaderboard("etf", "jjj", 57)

c4_result = db.get_leaderboard("c4")
etf_result = db.get_leaderboard("etf")
c4_passed = True
etf_passed = True
for i in range(len(c4_result) - 1):
    if c4_result[i] != len(c4_result):
        if c4_result[i][1] < c4_result[i + 1][1]:
            print("Test 6 failed, the scores are not from highest to lowest\nc4_result: ")
            print(c4_result)
            c4_passed = False
            break
    if etf_result[i] != len(etf_result) - 1:
        if etf_result[i][1] < etf_result[i + 1][1]:
            print("Test 6 failed, the scores are not from highest to lowest\netf_result: ")
            print(etf_result)
            etf_passed = False
            break

if c4_passed and etf_passed:
    tests_passed += 1
tests += 1

# test 7, add new scores that should not be added to the database
db.update_leaderboard("c4", "nog", 20)
db.update_leaderboard("etf", "nog", 10)

c4_result = db.get_leaderboard("c4")
etf_result = db.get_leaderboard("etf")
passed = True

for i in range(len(c4_result)):
    if c4_result[i] == ("nog", 20) or etf_result[i] == ("nog", 10):
        print("Test 7 failed, adding a highscore that does not make the top 10")
        print(c4_result)
        passed = False
        break
if passed:
    tests_passed += 1
tests += 1


# test 8, add score that makes top 10
db.update_leaderboard("c4", "new", 70)
db.update_leaderboard("etf", "new", 70)

c4_result = db.get_leaderboard("c4")
etf_result = db.get_leaderboard("etf")

# have we found the new scores in the leaderboard?
new_c4 = False
new_etf = False
# check if new score exists and if previous lowest score is deleted
for i in range(len(c4_result)):
    if c4_result[i] == ("aaa", 50) or etf_result[i] == ("aaa", 40):   # previous lowest which should no longer exist
        print("Test 8 failed, previous lowest high score was not deleted when adding the new one")
        print(c4_result)
        break
    if c4_result[i] == ("new", 70):
        new_c4 = True
    if etf_result[i] == ("new", 70):
        new_etf = True

if new_c4 and new_etf:
    tests_passed += 1
else:
    print("Test 8 failed, did not find the new scores in the leaderboard")
tests += 1



# test 9, adding a score that will be the new high score
db.update_leaderboard("c4", "top", 1000)
db.update_leaderboard("etf", "top", 1000)

c4_result = db.get_leaderboard("c4")
etf_result = db.get_leaderboard("etf")
if c4_result[0] == ("top", 1000) and etf_result[0] == ("top", 1000):
    tests_passed += 1
else:
    print("Test 9 failed, the new score should have been first but it is not\nc4_result:")
    print(c4_result)
    print("etf_result: ")
    print(etf_result)
tests += 1



# test 10, the high score is not added if the name matches another in the leaderboard, no errors caused
c4_result = db.update_leaderboard("c4", "top", 67)
etf_result = db.update_leaderboard("etf", "top", 67)
if c4_result == 0 or etf_result == 0:
    print("Test 10 failed, function did not return 1 when the score should not have been inserted")

c4_result = db.get_leaderboard("c4")
etf_result = db.get_leaderboard("etf")
passed = True
for i in range(len(c4_result)):
    if c4_result[i] == ("top", 67) or etf_result[i] == ("top", 67):
        print("Test 10 failed, the score should not have been inserted but it was")
        passed = False
if passed:
    tests_passed += 1
tests += 1


##################
# Settings tests #
##################

# test 11, test if changes to settings are saved
db.update_settings(music=75)
result = db.get_settings()
if result["music"] != 75:
    print("Test 11 failed, setting was not updated")
else:
    tests_passed += 1
tests += 1


# test 12, updating multiple settings at once
before = db.get_settings()
db.update_settings(music=100, sound=100, height=1280)
after = db.get_settings()
if (after["music"] == 100 and after["music"] != before["music"]) and \
    (after["sound"] == 100 and after["sound"] != before["sound"]) and \
    (after["res_height"] == 1280 and after["res_height"] != before["res_height"]):
    tests_passed += 1
else:
    print("Test 12 failed, not all of the settings were updated\nbefore: ")
    print(before)
    print("after: ")
    print(after)
tests += 1


###############
# Stats tests #
###############

# test 13, playing the first game of connect four
passed = False
db.update_stats("c4", 1, {"pieces_placed": 15, "almost_wins": 1, "score": 5000})
result = db.get_stats()
if result["games_played"] == 1 and result["games_won"] == 1 and math.isclose(1.0, result["win_percentage"], abs_tol=0.01):
    if result["c4_games"] == 1 and result["c4_wins"] == 1 and math.isclose(result["c4_percentage"], 1.0, abs_tol=0.01):
        if result["c4_pieces_placed"] == 15 and result["c4_almost_wins"] == 1 and result["total_score"] == 5000:
            # check to make sure etf stats weren't updated too (just checking this one time)
            if result["etf_games"] == 0 and result["etf_wins"] == 0 and math.isclose(result["etf_percentage"], 0, abs_tol=0.01):
                passed = True
if not passed:
    print("Test 13 failed, stats updated incorrectly after a c4 win\nresult: ")
    print(result)
else:
    tests_passed += 1
tests += 1


# test 14, add first loss to connect four
passed = False
db.update_stats("c4", 0, {"pieces_placed": 5, "almost_wins": 0, "score": 10})
result = db.get_stats()
if result["games_played"] == 2 and result["games_won"] == 1 and math.isclose(result["win_percentage"], 0.5, abs_tol=0.01):
    if result["c4_games"] == 2 and result["c4_wins"] == 1 and math.isclose(result["c4_percentage"], 0.5, abs_tol=0.01):
        if result["c4_pieces_placed"] == 20 and result["c4_almost_wins"] == 1 and result["total_score"] == 5010:
            passed = True
if passed:
    tests_passed += 1
else:
    print("Test 14 failed, stats incorrectly updated after c4 loss\nresult: ")
    print(result)
tests += 1

# test 15, first win for etf
passed = False
db.update_stats("etf", 1, {"score": 500, "fire_paths": 2, "water_paths": 5})
result = db.get_stats()
if result["games_played"] == 3 and result["games_won"] == 2 and math.isclose(result["win_percentage"], 0.666, abs_tol=0.01):
    if result["etf_games"] == 1 and result["etf_wins"] == 1 and math.isclose(result["etf_percentage"], 1.0, abs_tol=0.01):
        if result["total_score"] == 5510 and result["etf_fire_paths"] == 2 and result["etf_water_paths"] == 5:
            passed = True
if passed:
    tests_passed += 1
else:
    print("Test 15 failed, stats incorrectly updated after etf win\nresult: ")
    print(result)
tests += 1


# test 16, first loss for etf
passed = False
db.update_stats("etf", 0, {"score": 50, "fire_paths": 8, "water_paths": 1})
result = db.get_stats()
if result["games_played"] == 4 and result["games_won"] == 2 and math.isclose(result["win_percentage"], 0.5, abs_tol=0.01):
    if result["etf_games"] == 2 and result["etf_wins"] == 1 and math.isclose(result["etf_percentage"], 0.5, abs_tol=0.01):
        if result["total_score"] == 5560 and result["etf_fire_paths"] == 10 and result["etf_water_paths"] == 6:
            passed = True
if passed:
    tests_passed += 1
else:
    print("Test 16 failed, stats incorrectly updated after etf loss\nresult: ")
    print(result)
tests += 1


# test 17, game states can successfully be saved
state = [1, 2, 3, 4, 5, 6, 7, 8, 9]
db.save_game_state("c4", state)
result = db.get_game_state("c4")
if result == state:
    tests_passed += 1
else:
    print("Test 17 failed, game state was no successfully saved and retrieved\nresult: ")
    print(result)
tests += 1


# test 18, delete existing game state
db.delete_game_state("c4")
if db.get_game_state("c4") is None:
    tests_passed += 1
else:
    print("Test 18 failed, game state was not successfully deleted\nresult: ")
    print(result)
tests += 1

print("*** Test Script Complete ***")
print("Passed %d out of %d tests" % (tests_passed, tests))
