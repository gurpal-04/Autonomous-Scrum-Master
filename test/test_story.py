from firestore import story

# ---------- CREATE ----------
story_data = {
    "title": "User Authentication",
    "description": "Implement login/logout functionality",
    "epic_id": "epic123",
    "status": "todo",
    "assigned_to": "John Doe"
}
story_id = story.create_story(story_data)
print(f"[+] Created story with ID: {story_id}")

# ---------- GET ----------
fetched = story.get_story(story_id)
print(f"[✓] Fetched story: {fetched}")

# ---------- UPDATE ----------
story.update_story(story_id, {"status": "in-progress"})
print("[~] Updated status to in-progress")

# ---------- ADD COMMENT ----------
comment_id = story.add_comment(story_id, {"author": "Alice", "text": "This needs testing."})
print(f"[+] Comment added: {comment_id}")

# ---------- GET COMMENTS ----------
comments = story.get_comments(story_id)
print(f"[✓] Comments: {comments}")

# ---------- ACTIVITY LOG ----------
activity_id = story.log_activity(story_id, {"action": "status change", "by": "admin"})
print(f"[+] Activity logged: {activity_id}")

# ---------- GET ACTIVITY ----------
activity_log = story.get_activity_log(story_id)
print(f"[✓] Activity log: {activity_log}")

# ---------- LIST ALL ----------
all_stories = story.list_stories()
print(f"[📋] All stories: {all_stories}")

# ---------- DELETE ----------
# story.delete_story(story_id)
# print(f"[-] Deleted story: {story_id}")
