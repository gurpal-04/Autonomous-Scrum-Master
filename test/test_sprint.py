from firestore import sprint

# ---------- CREATE ----------
sprint_data = {
    "name": "Sprint 1",
    "goal": "Complete onboarding flow",
    "start_date": "2025-06-01",
    "end_date": "2025-06-15"
}
sprint_id = sprint.create_sprint(sprint_data)
print(f"[+] Created sprint with ID: {sprint_id}")

# ---------- GET ----------
fetched = sprint.get_sprint(sprint_id)
print(f"[✓] Fetched sprint: {fetched}")

# ---------- UPDATE ----------
sprint.update_sprint(sprint_id, {"goal": "Complete onboarding + dashboard"})
print("[~] Updated goal")

# ---------- ADD COMMENT ----------
comment_id = sprint.add_comment(sprint_id, {"author": "PM", "text": "Let's push dashboard to next sprint."})
print(f"[+] Comment added: {comment_id}")

# ---------- GET COMMENTS ----------
comments = sprint.get_comments(sprint_id)
print(f"[✓] Comments: {comments}")

# ---------- ACTIVITY LOG ----------
activity_id = sprint.log_activity(sprint_id, {"action": "updated goal", "by": "PM"})
print(f"[+] Activity logged: {activity_id}")

# ---------- GET ACTIVITY ----------
activity_log = sprint.get_activity_log(sprint_id)
print(f"[✓] Activity log: {activity_log}")

# ---------- LIST ALL ----------
all_sprints = sprint.list_sprints()
print(f"[📋] All sprints: {all_sprints}")

# ---------- DELETE ----------
# sprint.delete_sprint(sprint_id)
# print(f"[-] Deleted sprint: {sprint_id}")
