import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)

    user_display_name  = user['name']
    user_email         = user['email']
    user_handle        = user['preferred_username']
    user_cognito_id    = user['sub']
    
    conn = None  # Initialize conn to None
    
    try:
        print('entered-try')
        sql = f"""
            INSERT INTO public.users (
                display_name, 
                email,
                handle, 
                cognito_user_id
            ) 
            VALUES(%s,%s,%s,%s)
        """
        print('SQL Statement ----')
        print(sql)
        
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))  # Connect to the DB
        cur = conn.cursor()
        params = [
            user_display_name,
            user_email,
            user_handle,
            user_cognito_id
        ]
        cur.execute(sql, *params)
        conn.commit()  # Commit changes to DB

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error occurred: {error}")
    
    finally:
        if conn is not None:
            cur.close()
            conn.close()  # Close the connection if it was successfully created
            print('Database connection closed.')
    
    return event
