# AkBKukU Discord bot Postgres Schema/Table Configuration

One day I'll make the bot do this automatically, but for now:

## Schemas

Our system has two schemas, production and staging. But you can just make one if you wish, we named ours production:

## Tables

There's (currently) three tables in our schemas:
    
    - activity - Actions performed by members/staff
    - members - used for keeping information about users, i.e if they've been warned previously in the guild.
    - moderation - moderation events, i.e user warnings, kicks & bans.
    - options - Used for storing settings for the bot.

## Columns

Layout:
column_name | Datatype | Comment/Reason

### Table: Activity

    - action_id | integer | ID of the action (primary key)
    - guild_id | varchar(18) | ID of the guild the action happend in, limited to 18 characters.
    - action_type | varchar() | Action type, i.e MESSAGE_SENT, OPTIONS_MODIFIED etc.
    - action_executor | varchar(18) | ID of the user that performed the action, limited to 18 characters.
    - action_data | varchar() | Information about the action, i.e MESSAGE_CONTENT - Will usually be in JSON format.
    - action_timestamp | timestamp | ISO 8601 timestamp denotating when the task was performed.

### Table: Members

    - user_id | varchar(18) | ID of the member (primary key)
    - is_verified | boolean | (If used) if the member has been through the verification process (atleast once)
    - warnings | integer | How many warnings (including expired warnings) the user has had since joining.
    - is_monitored | boolean | If the user is marked as being monitored, i.e has broken a rule in the past

### Table: Moderation

    - moderation_event_id | integer | Primary key & Auto increment - Used for tracking the event.
    - guild_id | varchar(18) | ID of the guild the event took place in.
    - moderator_user_id | varchar(18) | ID of the mod/admin that created the event.
    - target_user_id | varchar(18) | Id of the user the event is targeted at.
    - moderation_event_type | varchar() | Event type name, i.e USER_BANNED, USER_KICKED, USER_WARNED etc.
    - moderation_event_expire | timestamp | The time the event expires (i.e temp ban, temp mute etc) - left NULL for permanent.
    - moderation_event_details | varchar() | A comment on the event (i.e "User broke rule 6 multiple times")
    - moderation_event_timestamp | timestamp | Timestamp that the moderation event took place at.

### Table: Options

    - guild_id | varchar(18) | ID of the guild the option belongs to
    - setting_name | varchar() | Name of the option - i.e VERIFICATION_ENABLED, VERIFICATION_PASSWORD etc.
    - setting_options | varchar() | Optional additional information to the setting, probably in JSON.
    - setting_creator | varchar(18) | ID of the user that orginally created the setting.
    - setting_last_edited_by | varchar(18) | ID of the user that last modified the options.