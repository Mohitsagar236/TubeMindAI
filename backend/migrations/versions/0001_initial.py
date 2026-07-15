"""Initial TubeMind schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def timestamps():
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade():
    op.create_table("users", sa.Column("id", sa.String(36), primary_key=True), sa.Column("email", sa.String(320), unique=True), sa.Column("name", sa.String(200)), *timestamps())
    op.create_table(
        "videos", sa.Column("id", sa.String(36), primary_key=True), sa.Column("youtube_video_id", sa.String(20), nullable=False, unique=True),
        sa.Column("youtube_url", sa.Text(), nullable=False), sa.Column("title", sa.Text()), sa.Column("channel_name", sa.Text()),
        sa.Column("thumbnail_url", sa.Text()), sa.Column("duration_seconds", sa.Integer()), sa.Column("language", sa.String(32)),
        sa.Column("transcript_status", sa.String(20), nullable=False), sa.Column("indexed_status", sa.String(20), nullable=False),
        sa.Column("error_message", sa.Text()), *timestamps())
    op.create_index("ix_videos_youtube_video_id", "videos", ["youtube_video_id"])
    op.create_table(
        "transcript_chunks", sa.Column("id", sa.String(36), primary_key=True), sa.Column("video_id", sa.String(36), sa.ForeignKey("videos.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False), sa.Column("text", sa.Text(), nullable=False), sa.Column("start_time_seconds", sa.Float()),
        sa.Column("end_time_seconds", sa.Float()), sa.Column("metadata_json", sa.JSON()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("video_id", "chunk_index"))
    op.create_index("ix_transcript_chunks_video_id", "transcript_chunks", ["video_id"])
    op.create_table(
        "chat_sessions", sa.Column("id", sa.String(36), primary_key=True), sa.Column("video_id", sa.String(36), sa.ForeignKey("videos.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id")), sa.Column("title", sa.Text()), *timestamps())
    op.create_index("ix_chat_sessions_video_id", "chat_sessions", ["video_id"])
    op.create_table(
        "chat_messages", sa.Column("id", sa.String(36), primary_key=True), sa.Column("chat_session_id", sa.String(36), sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("sources_json", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_chat_messages_chat_session_id", "chat_messages", ["chat_session_id"])
    op.create_table("generated_summaries", sa.Column("id", sa.String(36), primary_key=True), sa.Column("video_id", sa.String(36), sa.ForeignKey("videos.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id")), sa.Column("summary_type", sa.String(30), nullable=False), sa.Column("content", sa.Text(), nullable=False), *timestamps())
    op.create_table("generated_notes", sa.Column("id", sa.String(36), primary_key=True), sa.Column("video_id", sa.String(36), sa.ForeignKey("videos.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id")), sa.Column("title", sa.Text(), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("format", sa.String(30), nullable=False), *timestamps())
    op.create_table("generated_quizzes", sa.Column("id", sa.String(36), primary_key=True), sa.Column("video_id", sa.String(36), sa.ForeignKey("videos.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id")), sa.Column("quiz_json", sa.JSON(), nullable=False), *timestamps())
    op.create_table("generated_flashcards", sa.Column("id", sa.String(36), primary_key=True), sa.Column("video_id", sa.String(36), sa.ForeignKey("videos.id", ondelete="CASCADE"), nullable=False), sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id")), sa.Column("flashcards_json", sa.JSON(), nullable=False), *timestamps())
    for table in ("generated_summaries", "generated_notes", "generated_quizzes", "generated_flashcards"):
        op.create_index(f"ix_{table}_video_id", table, ["video_id"])


def downgrade():
    for table in ("generated_flashcards", "generated_quizzes", "generated_notes", "generated_summaries", "chat_messages", "chat_sessions", "transcript_chunks", "videos", "users"):
        op.drop_table(table)
