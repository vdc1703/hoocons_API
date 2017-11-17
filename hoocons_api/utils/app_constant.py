# Gender Constant
G_MALE = "Male"
G_FEMALE = "Female"
G_OTHER = "Other"
GENDER = ((G_MALE, 'Male'), (G_FEMALE,'Female'), (G_OTHER,'Other'))

# Relationship Status
R_FRIEND = "Friend"                      # Normal Friend
R_FOLLOWED = "Followed"                  # Followed user
R_FRIEND_FOLLOWED = "Friend_Followed"    # Best friend, send notif when friend posts
R_FRIEND_IGNORED = "Friend_Ignored"      # Do not show anything of friend's activity
R_BLOCKED = "Blocked"                    # Block user (other user won't see anything from me)
R_IGNORED = "Ignored" 					 # Ignore user (other user might see something from me)

RELATIONSHIP = (
    (R_FRIEND, "FRIEND"),
    (R_FOLLOWED, "FOLLOWED"),
    (R_FRIEND_FOLLOWED, "FRIEND_FOLLOWED"),
    (R_FRIEND_IGNORED, "FRIEND_FOLLOWED"),
    (R_BLOCKED, "BLOCKED"),
    (R_IGNORED, "IGNORED"),
)

CHATROOM_SINGLE = "csingle"
CHATROOM_GROUP = "cgroup"

CHATROOM = (
    (CHATROOM_SINGLE, "ROOM_SINGLE"),
    (CHATROOM_GROUP, "ROOM_GROUP")
)