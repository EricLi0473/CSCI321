from Entity.individualAccount import IndividualAccount


def update_bio(user_id, bio):
    try:
        # Replace with actual database update logic
        user = IndividualAccount().findOneAccount(user_id)
        if user:
            user['bio'] = bio
            # Save the updated user back to the database
            IndividualAccount().updateAccount(user)
            return True
    except Exception as e:
        print(f"Error updating bio: {e}")
    return False