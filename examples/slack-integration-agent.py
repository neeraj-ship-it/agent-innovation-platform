#!/usr/bin/env python3
"""
Slack Integration Agent - Posts updates to Slack
Connects AMAIP with Slack workspace
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent

# Uncomment to use:
# pip install slack-sdk
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError


class SlackAgent(Agent):
    """Agent that posts AMAIP activity to Slack"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup Slack client (uncomment to use)
        # self.slack = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        # self.channel = "#amaip-activity"

    def on_start(self):
        print(f"💬 Slack Agent ready! Will post to Slack channel")
        # self.post_to_slack("🤖 AMAIP Slack Agent is now online!")

    def on_task_created(self, task):
        """Post task creation to Slack"""
        message = f"📋 New Task: *{task['title']}*\\nCreated by: {task.get('creator_name', 'Unknown')}"
        print(f"💬 Would post to Slack: {message}")
        # self.post_to_slack(message)

    def on_task_assigned(self, task):
        """Post task assignment to Slack"""
        message = f"👉 Task Assigned: *{task['title']}* → {task.get('assigned_name')}"
        print(f"💬 Would post to Slack: {message}")
        # self.post_to_slack(message)

    def on_innovation_created(self, innovation):
        """Post innovation to Slack"""
        message = f"""
✨ *New Innovation!*
Title: {innovation['title']}
Category: {innovation.get('category', 'N/A')}
WOW Score: {'⭐' * innovation.get('wow_score', 0)}
"""
        print(f"💬 Would post to Slack: {message}")
        # self.post_to_slack(message, blocks=self.create_innovation_blocks(innovation))

    def post_to_slack(self, text, blocks=None):
        """Post message to Slack (uncomment to use)"""
        # try:
        #     self.slack.chat_postMessage(
        #         channel=self.channel,
        #         text=text,
        #         blocks=blocks
        #     )
        # except SlackApiError as e:
        #     print(f"Error posting to Slack: {e.response['error']}")
        pass

    def create_innovation_blocks(self, innovation):
        """Create rich Slack blocks for innovation"""
        return [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "✨ New Innovation!"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Title:*\\n{innovation['title']}"},
                    {"type": "mrkdwn", "text": f"*Category:*\\n{innovation.get('category', 'N/A')}"}
                ]
            }
        ]


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║              SLACK INTEGRATION AGENT                   ║
    ╠════════════════════════════════════════════════════════╣
    ║  To enable:                                            ║
    ║  1. pip install slack-sdk                              ║
    ║  2. Create Slack App & get bot token                   ║
    ║  3. export SLACK_BOT_TOKEN="xoxb-..."                 ║
    ║  4. Uncomment Slack code in this file                  ║
    ╚════════════════════════════════════════════════════════╝
    """)

    agent = SlackAgent(
        name="SlackBot",
        capabilities=["slack", "integration", "notifications"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print("\\n\\n💬 Slack Agent shutting down...")
        agent.stop()


if __name__ == "__main__":
    main()
