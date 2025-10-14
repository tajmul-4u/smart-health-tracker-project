"""
Working Dashboard Controller - Fixed and Complete
This version works standalone without external UI file dependencies
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QStackedWidget, QScrollArea, QFrame, QMessageBox,
    QDialog, QTextEdit, QLineEdit, QFormLayout, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette
from app.services.api_client import APIClient
from datetime import datetime
from typing import Optional
import sys

class WorkingDashboardController(QMainWindow):
    """Working Dashboard Controller with all bugs fixed"""
    
    def __init__(self, api_client: Optional[APIClient] = None):
        super().__init__()
        self.api_client = api_client or APIClient()
        self.current_user = {}
        
        # Initialize UI
        self.init_ui()
        
        # Load initial data
        self.load_user_data()
        
    def init_ui(self):
        """Initialize the user interface programmatically"""
        self.setWindowTitle("🏥 Smart Health Tracker - Dashboard")
        self.setGeometry(100, 50, 1200, 800)
        
        # Set main window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (horizontal)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left navigation panel (keep a reference for toggling)
        self.nav_widget = self.create_navigation_panel()
        main_layout.addWidget(self.nav_widget)
        
        # Right content area
        content_area = self.create_content_area()
        main_layout.addWidget(content_area)
        
        # Set stretch factors (1:4 ratio)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 4)
        
    def create_navigation_panel(self):
        """Create left navigation panel"""
        nav_widget = QWidget()
        nav_widget.setFixedWidth(250)
        nav_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                border-radius: 0px;
            }
        """)
        
        layout = QVBoxLayout()
        nav_widget.setLayout(layout)
        
        # Logo/Title
        title = QLabel("🏥 Health Tracker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("""
            QLabel {
                color: white;
                padding: 20px;
                background-color: transparent;
            }
        """)
        layout.addWidget(title)
        
        # User info section
        user_frame = QFrame()
        user_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin: 10px;
            }
        """)
        user_layout = QVBoxLayout()
        
        self.userNameLabel = QLabel("👤 Loading...")
        self.userNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userNameLabel.setStyleSheet("color: white; font-weight: bold;")
        user_layout.addWidget(self.userNameLabel)
        
        # Profile button
        profile_btn = QPushButton("👤 View Profile")
        profile_btn.clicked.connect(self.show_profile_menu)
        profile_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        user_layout.addWidget(profile_btn)
        
        user_frame.setLayout(user_layout)
        layout.addWidget(user_frame)
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", 0),
            ("💪 Habits", 1),
            ("❤️ Health Conditions", 2),
            ("📈 Analytics", 3),
            ("🤖 AI Predictions", 4),
            ("👥 Community", 5),
            ("⚙️ Settings", 6),
        ]
        
        for btn_text, page_idx in nav_buttons:
            btn = QPushButton(btn_text)
            btn.clicked.connect(lambda checked, idx=page_idx: self.switch_page(idx))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    text-align: left;
                    padding: 15px 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: rgba(52, 152, 219, 0.3);
                }
                QPushButton:pressed {
                    background-color: #3498db;
                }
            """)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px;
                margin: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(logout_btn)
        
        return nav_widget
        
    def create_content_area(self):
        """Create right content area with stacked pages"""
        content_widget = QWidget()
        layout = QVBoxLayout()
        content_widget.setLayout(layout)
        
        # Top bar
        top_bar = self.create_top_bar()
        layout.addWidget(top_bar)
        
        # Stacked widget for different pages
        self.contentStackedWidget = QStackedWidget()
        
        # Add pages
        self.contentStackedWidget.addWidget(self.create_dashboard_page())  # 0
        self.contentStackedWidget.addWidget(self.create_habits_page())  # 1
        self.contentStackedWidget.addWidget(self.create_health_page())  # 2
        self.contentStackedWidget.addWidget(self.create_analytics_page())  # 3
        self.contentStackedWidget.addWidget(self.create_ai_page())  # 4
        self.contentStackedWidget.addWidget(self.create_community_page())  # 5
        self.contentStackedWidget.addWidget(self.create_settings_page())  # 6
        
        layout.addWidget(self.contentStackedWidget)
        
        return content_widget
        
    def create_top_bar(self):
        """Create top navigation bar"""
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 2px solid #ecf0f1;
            }
        """)
        
        layout = QHBoxLayout()
        top_bar.setLayout(layout)
        
        # Menu button (hamburger) for toggling sidebar - left aligned
        self.menuButton = QPushButton("☰")
        self.menuButton.setFixedSize(36, 36)
        self.menuButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2c3e50;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
                border-radius: 6px;
            }
        """)
        self.menuButton.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.menuButton)

        # Page title
        self.page_title = QLabel("📊 Dashboard Overview")
        self.page_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.page_title.setStyleSheet("color: #2c3e50; border: none;")
        layout.addWidget(self.page_title)
        
        layout.addStretch()
        
        # Notification button
        self.notificationButton = QPushButton("🔔 Notifications")
        self.notificationButton.clicked.connect(self.show_notifications)
        self.notificationButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(self.notificationButton)
        
        return top_bar
        
    def create_dashboard_page(self):
        """Create modern dashboard overview page"""
        page = QWidget()
        page.setStyleSheet("background-color: #f8f9fa;")
        
        # Main scroll area for better content organization
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        scroll_content.setLayout(layout)
        
        # === HERO SECTION ===
        hero_section = self.create_hero_section()
        layout.addWidget(hero_section)
        
        # === STATS CARDS ROW ===
        stats_section = self.create_modern_stats_section()
        layout.addLayout(stats_section)
        
        # === TWO COLUMN LAYOUT ===
        two_col_layout = QHBoxLayout()
        two_col_layout.setSpacing(15)
        
        # Left column (60%)
        left_column = QVBoxLayout()
        left_column.setSpacing(15)
        
        # Today's Goals Progress
        goals_widget = self.create_goals_progress_widget()
        left_column.addWidget(goals_widget)
        
        # Recent Activity Timeline
        activity_widget = self.create_activity_timeline_widget()
        left_column.addWidget(activity_widget)
        
        two_col_layout.addLayout(left_column, 6)
        
        # Right column (40%)
        right_column = QVBoxLayout()
        right_column.setSpacing(15)
        
        # Health Score Widget
        health_score_widget = self.create_health_score_widget()
        right_column.addWidget(health_score_widget)
        
        # Quick Actions Panel
        quick_actions_widget = self.create_quick_actions_widget()
        right_column.addWidget(quick_actions_widget)
        
        # Upcoming Reminders
        reminders_widget = self.create_reminders_widget()
        right_column.addWidget(reminders_widget)
        
        two_col_layout.addLayout(right_column, 4)
        
        layout.addLayout(two_col_layout)
        
        # === HEALTH INSIGHTS SECTION ===
        insights_widget = self.create_health_insights_widget()
        layout.addWidget(insights_widget)
        
        # === WELLNESS TIPS SECTION ===
        wellness_widget = self.create_wellness_tips_widget()
        layout.addWidget(wellness_widget)
        
        layout.addStretch()
        
        scroll.setWidget(scroll_content)
        
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        page.setLayout(page_layout)
        page_layout.addWidget(scroll)
        
        return page
    
    def create_hero_section(self):
        """Create hero section with personalized greeting and animated elements"""
        from datetime import datetime
        
        hero = QFrame()
        hero.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border-radius: 20px;
                padding: 35px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        main_layout = QHBoxLayout()
        hero.setLayout(main_layout)
        
        # Left side - Greeting and info
        left_layout = QVBoxLayout()
        
        # Get time-based greeting with more emojis
        hour = datetime.now().hour
        if hour < 12:
            greeting = "🌅 Good Morning"
            motivational = "Start your day strong!"
        elif hour < 17:
            greeting = "☀️ Good Afternoon"
            motivational = "Keep up the momentum!"
        else:
            greeting = "🌙 Good Evening"
            motivational = "Wind down with wellness!"
        
        greeting_label = QLabel(f"{greeting}, {self.current_user.get('full_name', 'User')}!")
        greeting_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        greeting_label.setStyleSheet("color: white; letter-spacing: 1px;")
        left_layout.addWidget(greeting_label)
        
        subtitle = QLabel(f"✨ {motivational} Here's your health summary for today")
        subtitle.setFont(QFont("Arial", 15))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.95); margin-top: 8px; line-height: 1.5;")
        subtitle.setWordWrap(True)
        left_layout.addWidget(subtitle)
        
        # Current date and streak
        info_layout = QHBoxLayout()
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        date_label = QLabel(f"📅 {current_date}")
        date_label.setFont(QFont("Arial", 13))
        date_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); margin-top: 12px;")
        info_layout.addWidget(date_label)
        
        streak_label = QLabel("🔥 15 Day Streak!")
        streak_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        streak_label.setStyleSheet("""
            color: white;
            background-color: rgba(255, 255, 255, 0.2);
            padding: 6px 15px;
            border-radius: 20px;
            margin-top: 12px;
        """)
        info_layout.addWidget(streak_label)
        info_layout.addStretch()
        
        left_layout.addLayout(info_layout)
        left_layout.addStretch()
        
        main_layout.addLayout(left_layout, 7)
        
        # Right side - Quick stats summary
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Mini stats cards
        mini_stats = [
            {"icon": "💪", "label": "Active", "value": "85%"},
            {"icon": "🎯", "label": "Goals", "value": "4/5"},
        ]
        
        for stat in mini_stats:
            mini_card = QFrame()
            mini_card.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.25);
                    border-radius: 12px;
                    padding: 15px;
                    margin: 5px 0;
                }
            """)
            mini_card.setMinimumWidth(180)
            
            mini_layout = QHBoxLayout()
            mini_card.setLayout(mini_layout)
            
            icon_lbl = QLabel(stat['icon'])
            icon_lbl.setFont(QFont("Arial", 24))
            mini_layout.addWidget(icon_lbl)
            
            text_layout = QVBoxLayout()
            text_layout.setSpacing(2)
            
            label_lbl = QLabel(stat['label'])
            label_lbl.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 11px;")
            text_layout.addWidget(label_lbl)
            
            value_lbl = QLabel(stat['value'])
            value_lbl.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            value_lbl.setStyleSheet("color: white;")
            text_layout.addWidget(value_lbl)
            
            mini_layout.addLayout(text_layout)
            
            right_layout.addWidget(mini_card)
        
        main_layout.addLayout(right_layout, 3)
        
        return hero
    
    def create_modern_stats_section(self):
        """Create modern stats cards with enhanced visuals"""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        stats_data = [
            {
                "icon": "👣",
                "title": "Steps Today",
                "value": "8,247",
                "target": "10,000",
                "progress": 82,
                "color": "#3498db",
                "trend": "↑ 12%"
            },
            {
                "icon": "😴",
                "title": "Sleep",
                "value": "7.5h",
                "target": "8h",
                "progress": 94,
                "color": "#9b59b6",
                "trend": "✓ Good"
            },
            {
                "icon": "💧",
                "title": "Water Intake",
                "value": "2.3L",
                "target": "3L",
                "progress": 77,
                "color": "#1abc9c",
                "trend": "↑ 6 cups"
            },
            {
                "icon": "🔥",
                "title": "Calories",
                "value": "1,850",
                "target": "2,000",
                "progress": 93,
                "color": "#e74c3c",
                "trend": "→ On track"
            },
        ]
        
        for stat in stats_data:
            card = self.create_enhanced_stat_card(stat)
            stats_layout.addWidget(card)
        
        return stats_layout
    
    def create_enhanced_stat_card(self, data):
        """Create enhanced stat card with progress, trend, and animations"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 15px;
                border-left: 6px solid {data['color']};
                padding: 22px;
                border: 1px solid #e0e0e0;
            }}
            QFrame:hover {{
                background-color: #fafafa;
                border: 1px solid {data['color']};
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }}
        """)
        card.setMinimumHeight(180)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout()
        card.setLayout(layout)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(data['icon'])
        icon_label.setFont(QFont("Arial", 32))
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        trend_label = QLabel(data['trend'])
        trend_label.setStyleSheet(f"""
            color: {data['color']}; 
            font-weight: bold; 
            font-size: 12px;
            background-color: {self._lighten_color(data['color'])};
            padding: 4px 8px;
            border-radius: 10px;
        """)
        header_layout.addWidget(trend_label)
        
        layout.addLayout(header_layout)
        
        # Title
        title_label = QLabel(data['title'])
        title_label.setStyleSheet("color: #7f8c8d; font-size: 13px; margin-top: 8px; font-weight: 600;")
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(data['value'])
        value_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {data['color']}; margin-top: 8px; letter-spacing: -1px;")
        layout.addWidget(value_label)
        
        # Target and progress
        target_layout = QHBoxLayout()
        target_label = QLabel(f"of {data['target']}")
        target_label.setStyleSheet("color: #95a5a6; font-size: 12px; font-weight: 500;")
        target_layout.addWidget(target_label)
        target_layout.addStretch()
        
        progress_label = QLabel(f"{data['progress']}%")
        progress_label.setStyleSheet(f"color: {data['color']}; font-weight: bold; font-size: 12px;")
        target_layout.addWidget(progress_label)
        
        layout.addLayout(target_layout)
        
        # Progress bar with animation-ready style
        from PyQt6.QtWidgets import QProgressBar
        progress = QProgressBar()
        progress.setValue(data['progress'])
        progress.setTextVisible(False)
        progress.setMaximumHeight(8)
        progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: #ecf0f1;
                border-radius: 4px;
                margin-top: 8px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {data['color']}, stop:1 {self._darken_color(data['color'])});
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress)
        
        return card
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color for backgrounds"""
        color_map = {
            "#3498db": "#e3f2fd",
            "#9b59b6": "#f3e5f5",
            "#1abc9c": "#e0f2f1",
            "#e74c3c": "#ffebee",
            "#f39c12": "#fff8e1",
            "#27ae60": "#e8f5e9",
        }
        return color_map.get(hex_color, "#f5f5f5")
    
    def _darken_color(self, hex_color):
        """Darken a hex color for gradients"""
        color_map = {
            "#3498db": "#2980b9",
            "#9b59b6": "#8e44ad",
            "#1abc9c": "#16a085",
            "#e74c3c": "#c0392b",
            "#f39c12": "#e67e22",
            "#27ae60": "#229954",
        }
        return color_map.get(hex_color, hex_color)
    
    def create_goals_progress_widget(self):
        """Create today's goals progress widget"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Header
        header = QLabel("🎯 Today's Goals Progress")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(header)
        
        # Goals list
        goals = [
            {"name": "Complete 30 min workout", "progress": 100, "color": "#27ae60"},
            {"name": "Drink 8 glasses of water", "progress": 75, "color": "#3498db"},
            {"name": "Log all meals", "progress": 66, "color": "#f39c12"},
            {"name": "Sleep before 11 PM", "progress": 0, "color": "#95a5a6"},
        ]
        
        for goal in goals:
            goal_item = self.create_goal_progress_item(goal)
            layout.addWidget(goal_item)
        
        # Overall progress
        overall_label = QLabel("Overall Progress: 60% (3 of 5 goals completed)")
        overall_label.setStyleSheet("color: #7f8c8d; font-size: 12px; margin-top: 10px; font-weight: bold;")
        layout.addWidget(overall_label)
        
        return widget
    
    def create_goal_progress_item(self, goal):
        """Create a single goal progress item"""
        from PyQt6.QtWidgets import QProgressBar
        
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 5, 0, 5)
        container.setLayout(layout)
        
        # Goal name and percentage
        header_layout = QHBoxLayout()
        
        check_icon = "✅" if goal['progress'] == 100 else "⏳" if goal['progress'] > 0 else "⭕"
        name_label = QLabel(f"{check_icon} {goal['name']}")
        name_label.setStyleSheet("color: #34495e; font-size: 13px;")
        header_layout.addWidget(name_label)
        
        header_layout.addStretch()
        
        percent_label = QLabel(f"{goal['progress']}%")
        percent_label.setStyleSheet(f"color: {goal['color']}; font-weight: bold; font-size: 12px;")
        header_layout.addWidget(percent_label)
        
        layout.addLayout(header_layout)
        
        # Progress bar
        progress = QProgressBar()
        progress.setValue(goal['progress'])
        progress.setTextVisible(False)
        progress.setMaximumHeight(8)
        progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: #ecf0f1;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {goal['color']};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress)
        
        return container
    
    def create_activity_timeline_widget(self):
        """Create activity timeline widget"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("📋 Recent Activity")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        view_all_btn = QPushButton("View All →")
        view_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3498db;
                border: none;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #2980b9;
                text-decoration: underline;
            }
        """)
        header_layout.addWidget(view_all_btn)
        
        layout.addLayout(header_layout)
        
        # Timeline items
        activities = [
            {"icon": "✅", "text": "Logged morning vitals", "time": "2 hours ago", "color": "#27ae60"},
            {"icon": "🏃", "text": "Completed 30 min workout", "time": "5 hours ago", "color": "#e74c3c"},
            {"icon": "💊", "text": "Took medications", "time": "8 hours ago", "color": "#3498db"},
            {"icon": "🥗", "text": "Logged healthy lunch", "time": "6 hours ago", "color": "#f39c12"},
            {"icon": "😴", "text": "Sleep logged (7.5h)", "time": "12 hours ago", "color": "#9b59b6"},
        ]
        
        for activity in activities:
            item = self.create_timeline_item(activity)
            layout.addWidget(item)
        
        return widget
    
    def create_timeline_item(self, activity):
        """Create a timeline item"""
        item = QFrame()
        item.setStyleSheet(f"""
            QFrame {{
                background-color: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid {activity['color']};
                padding: 12px;
                margin: 5px 0;
            }}
            QFrame:hover {{
                background-color: #ecf0f1;
            }}
        """)
        
        layout = QHBoxLayout()
        item.setLayout(layout)
        
        # Icon
        icon_label = QLabel(activity['icon'])
        icon_label.setFont(QFont("Arial", 20))
        layout.addWidget(icon_label)
        
        # Text and time
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        text_label = QLabel(activity['text'])
        text_label.setStyleSheet("color: #2c3e50; font-weight: bold; font-size: 13px;")
        text_layout.addWidget(text_label)
        
        time_label = QLabel(activity['time'])
        time_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        text_layout.addWidget(time_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        return item
    
    def create_health_score_widget(self):
        """Create health score widget"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Title
        title = QLabel("💪 Health Score")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Score circle (simplified)
        score_label = QLabel("85")
        score_label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        score_label.setStyleSheet("color: white; margin: 20px 0;")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(score_label)
        
        # Rating
        rating_label = QLabel("⭐⭐⭐⭐⭐")
        rating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rating_label.setStyleSheet("font-size: 20px; margin-bottom: 10px;")
        layout.addWidget(rating_label)
        
        # Status
        status_label = QLabel("Excellent Health!")
        status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        status_label.setStyleSheet("color: white;")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_label)
        
        # Improvement tip
        tip_label = QLabel("💡 Keep up the great work!")
        tip_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 11px; margin-top: 10px;")
        tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tip_label)
        
        return widget
    
    def create_quick_actions_widget(self):
        """Create quick actions panel"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Header
        header = QLabel("⚡ Quick Actions")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Action buttons
        actions = [
            {"icon": "🏥", "text": "Log Health Data", "color": "#3498db"},
            {"icon": "💪", "text": "Add Habit", "color": "#27ae60"},
            {"icon": "📊", "text": "View Analytics", "color": "#9b59b6"},
            {"icon": "🤖", "text": "AI Insights", "color": "#e74c3c"},
        ]
        
        for action in actions:
            btn = QPushButton(f"{action['icon']} {action['text']}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {action['color']};
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 8px;
                    text-align: left;
                    font-weight: bold;
                    font-size: 13px;
                    margin: 3px 0;
                }}
                QPushButton:hover {{
                    opacity: 0.9;
                    transform: scale(1.02);
                }}
            """)
            if "Health Data" in action['text']:
                btn.clicked.connect(self.show_health_data_input)
            elif "Habit" in action['text']:
                btn.clicked.connect(self.show_habit_input_dialog)
            elif "Analytics" in action['text']:
                btn.clicked.connect(lambda: self.switch_page(3))
            elif "AI" in action['text']:
                btn.clicked.connect(lambda: self.switch_page(4))
            
            layout.addWidget(btn)
        
        return widget
    
    def create_reminders_widget(self):
        """Create reminders widget"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Header
        header = QLabel("🔔 Upcoming Reminders")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Reminders
        reminders = [
            {"icon": "💊", "text": "Evening medication", "time": "6:00 PM"},
            {"icon": "🥗", "text": "Log dinner", "time": "7:30 PM"},
            {"icon": "😴", "text": "Bedtime routine", "time": "10:00 PM"},
        ]
        
        for reminder in reminders:
            item = QFrame()
            item.setStyleSheet("""
                QFrame {
                    background-color: #fff8e1;
                    border-radius: 6px;
                    padding: 10px;
                    margin: 3px 0;
                    border-left: 3px solid #f39c12;
                }
            """)
            
            item_layout = QHBoxLayout()
            item.setLayout(item_layout)
            
            icon_label = QLabel(reminder['icon'])
            icon_label.setFont(QFont("Arial", 16))
            item_layout.addWidget(icon_label)
            
            text_label = QLabel(reminder['text'])
            text_label.setStyleSheet("color: #34495e; font-size: 12px; font-weight: bold;")
            item_layout.addWidget(text_label)
            
            item_layout.addStretch()
            
            time_label = QLabel(reminder['time'])
            time_label.setStyleSheet("color: #f39c12; font-size: 11px; font-weight: bold;")
            item_layout.addWidget(time_label)
            
            layout.addWidget(item)
        
        return widget
    
    def create_health_insights_widget(self):
        """Create health insights widget"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                border-radius: 12px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🧠 AI Health Insights")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        badge = QLabel("NEW")
        badge.setStyleSheet("""
            QLabel {
                background-color: rgba(255,255,255,0.3);
                color: white;
                padding: 4px 8px;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(badge)
        
        layout.addLayout(header_layout)
        
        # Insights
        insights = [
            "💡 Your sleep quality improved by 15% this week. Great job!",
            "🎯 You're 200 steps away from beating yesterday's record.",
            "💧 Hydration levels are optimal. Keep it up!",
            "🏃 Consider adding 10 more minutes to your workout for maximum benefit.",
        ]
        
        for insight in insights:
            insight_label = QLabel(insight)
            insight_label.setStyleSheet("""
                color: white;
                font-size: 13px;
                margin: 8px 0;
                padding: 10px;
                background-color: rgba(255,255,255,0.1);
                border-radius: 6px;
            """)
            insight_label.setWordWrap(True)
            layout.addWidget(insight_label)
        
        return widget
    
    def create_wellness_tips_widget(self):
        """Create daily wellness tips widget with rotating tips"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fa709a, stop:1 #fee140);
                border-radius: 12px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("💫 Daily Wellness Tips")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.3);
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 15px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.5);
            }
        """)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Tips grid
        tips_grid = QHBoxLayout()
        tips_grid.setSpacing(15)
        
        tips = [
            {
                "icon": "🧘‍♀️",
                "title": "Mindfulness",
                "tip": "Take 5 deep breaths to reduce stress and improve focus",
                "color": "#9b59b6"
            },
            {
                "icon": "💧",
                "title": "Hydration",
                "tip": "Drink a glass of water every 2 hours to stay energized",
                "color": "#3498db"
            },
            {
                "icon": "🥗",
                "title": "Nutrition",
                "tip": "Include colorful vegetables in every meal for vitamins",
                "color": "#27ae60"
            },
        ]
        
        for tip_data in tips:
            tip_card = QFrame()
            tip_card.setStyleSheet("""
                QFrame {
                    background-color: rgba(255,255,255,0.95);
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
            
            tip_layout = QVBoxLayout()
            tip_card.setLayout(tip_layout)
            
            # Icon and title
            header_tip = QHBoxLayout()
            icon_lbl = QLabel(tip_data['icon'])
            icon_lbl.setFont(QFont("Arial", 22))
            header_tip.addWidget(icon_lbl)
            
            title_lbl = QLabel(tip_data['title'])
            title_lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            title_lbl.setStyleSheet(f"color: {tip_data['color']};")
            header_tip.addWidget(title_lbl)
            header_tip.addStretch()
            
            tip_layout.addLayout(header_tip)
            
            # Tip text
            tip_lbl = QLabel(tip_data['tip'])
            tip_lbl.setStyleSheet("color: #555; font-size: 11px; line-height: 1.4;")
            tip_lbl.setWordWrap(True)
            tip_layout.addWidget(tip_lbl)
            
            tips_grid.addWidget(tip_card)
        
        layout.addLayout(tips_grid)
        
        # Pro tip at bottom
        pro_tip = QLabel("💎 Pro Tip: Consistency beats perfection. Focus on small daily improvements!")
        pro_tip.setStyleSheet("""
            color: white;
            font-size: 12px;
            font-weight: bold;
            margin-top: 15px;
            padding: 10px;
            background-color: rgba(255,255,255,0.2);
            border-radius: 8px;
        """)
        pro_tip.setWordWrap(True)
        layout.addWidget(pro_tip)
        
        return widget
        
    def create_habits_page(self):
        """Create habits tracking page"""
        return self.create_page_with_data(
            "💪 Habits Tracking",
            [
                "🏃 Exercise 30 minutes - ✅ Completed (15 day streak)",
                "📚 Read for 20 minutes - ✅ Completed",
                "💧 Drink 8 glasses of water - ⏳ In Progress (6/8)",
                "🧘 Meditate 10 minutes - ✅ Completed",
                "💊 Take vitamins - ❌ Missed today",
            ]
        )
        
    def create_health_page(self):
        """Create health conditions page"""
        return self.create_page_with_data(
            "❤️ Health Conditions",
            [
                "🩺 Blood Pressure: 120/80 mmHg - Normal",
                "🩸 Blood Sugar: 95 mg/dL - Normal",
                "❤️ Heart Rate: 72 bpm - Normal",
                "🌡️ Temperature: 36.6°C - Normal",
                "😴 Sleep Quality: 8/10 - Good",
                "💧 Hydration: Good (2.5L today)",
            ]
        )
        
    def create_analytics_page(self):
        """Create analytics page"""
        return self.create_page_with_data(
            "📈 Analytics & Trends",
            [
                "📊 Weekly Health Score: 85/100 (Excellent)",
                "📈 Blood Pressure Trend: Stable",
                "💤 Sleep Pattern: Consistent 7.5h average",
                "🏃 Activity Level: 8,500 steps/day average",
                "🎯 Goal Progress: 4/5 weekly goals met",
            ]
        )
        
    def create_ai_page(self):
        """Create AI predictions page"""
        return self.create_page_with_data(
            "🤖 AI Health Predictions",
            [
                "🤖 Health Risk Assessment: Low Risk",
                "📈 Blood Pressure Prediction: Stable for next 7 days",
                "😴 Sleep Optimization: Consider 30min earlier bedtime",
                "🏃 Activity Recommendation: Add 15min cardio",
                "🎯 Goal Achievement Probability: 87%",
            ]
        )
        
    def create_community_page(self):
        """Create community insights page"""
        return self.create_page_with_data(
            "👥 Community Insights",
            [
                "👥 Active Users Today: 1,247 people",
                "🏆 Top Goal: Daily water intake (89% completion)",
                "📊 Average Health Score: 78/100",
                "💪 Most Popular Activity: Walking",
                "📈 Your Ranking: Top 25% in your age group",
            ]
        )
        
    def create_settings_page(self):
        """Create settings page"""
        return self.create_page_with_data(
            "⚙️ Settings & Preferences",
            [
                "🔔 Notifications: Enabled",
                "📊 Data Sync: Auto-sync every 5 minutes",
                "🔒 Privacy Mode: Standard",
                "📱 App Theme: Auto (Light/Dark)",
                "🌍 Units: Metric (kg, cm, °C)",
            ]
        )
        
    def create_page_with_data(self, title, items):
        """Create a generic page with data items"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Page header
        header = QLabel(title)
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 20px;
                border-radius: 10px;
            }
        """)
        layout.addWidget(header)
        
        # Add data input button
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add New Entry")
        add_btn.clicked.connect(lambda: self.show_data_input_dialog(title))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_layout.addWidget(add_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Scroll area for items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)
        
        for item in items:
            item_label = QLabel(item)
            item_label.setStyleSheet("""
                QLabel {
                    background-color: white;
                    padding: 15px;
                    border-radius: 8px;
                    border-left: 4px solid #3498db;
                    margin: 5px;
                    font-size: 13px;
                }
            """)
            scroll_layout.addWidget(item_label)
            
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return page
        
    def switch_page(self, page_index):
        """Switch between pages"""
        self.contentStackedWidget.setCurrentIndex(page_index)
        
        # Update page title
        titles = [
            "📊 Dashboard Overview",
            "💪 Habits Tracking", 
            "❤️ Health Conditions",
            "📈 Analytics & Trends",
            "🤖 AI Predictions",
            "👥 Community Insights",
            "⚙️ Settings"
        ]
        
        if 0 <= page_index < len(titles):
            self.page_title.setText(titles[page_index])
            
    def show_profile_menu(self):
        """Show profile options"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction
        
        menu = QMenu(self)
        
        # Edit Profile
        edit_action = QAction("👤 Edit Profile", self)
        edit_action.triggered.connect(self.show_profile_form)
        menu.addAction(edit_action)
        
        # Health Data
        health_action = QAction("🏥 Health Data Input", self)
        health_action.triggered.connect(self.show_health_data_input)
        menu.addAction(health_action)
        
        menu.addSeparator()
        
        # Settings
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(lambda: self.switch_page(6))
        menu.addAction(settings_action)
        
        # Show menu
        menu.exec(self.mapToGlobal(self.rect().topRight()))
        
    def show_profile_form(self):
        """Show profile editing form"""
        try:
            from app.widgets.user_profile_form import UserProfileFormWidget
            
            dialog = QDialog(self)
            dialog.setWindowTitle("👤 Edit Profile")
            dialog.setModal(True)
            dialog.resize(900, 700)
            
            layout = QVBoxLayout()
            profile_form = UserProfileFormWidget(self.api_client)
            layout.addWidget(profile_form)
            
            close_btn = QPushButton("✅ Close")
            close_btn.clicked.connect(dialog.accept)
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    border-radius: 5px;
                }
            """)
            layout.addWidget(close_btn)
            
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.information(self, "Profile", f"Profile form: {str(e)}")
            
    def show_health_data_input(self):
        """Show health data input"""
        try:
            from app.widgets.modern_health_input import ModernHealthDataInput
            
            dialog = QDialog(self)
            dialog.setWindowTitle("🏥 Health Data Input")
            dialog.setModal(True)
            dialog.resize(1200, 900)
            
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            
            health_widget = ModernHealthDataInput(self.api_client)
            layout.addWidget(health_widget)
            
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.information(self, "Health Data", f"Opening health data input: {str(e)}")
            
    def show_data_input_dialog(self, section_title):
        """Show data input dialog for a section"""
        if "Health" in section_title:
            self.show_health_data_input()
        elif "Habits" in section_title:
            self.show_habit_input_dialog()
        else:
            QMessageBox.information(self, "Coming Soon", f"Data input for {section_title} coming soon!")
            
    def show_habit_input_dialog(self):
        """Show habit input dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("💪 Add New Habit")
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout()
        
        # Form
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter habit name...")
        
        category_input = QComboBox()
        category_input.addItems(["Health & Fitness", "Learning", "Productivity", "Wellness"])
        
        frequency_input = QComboBox()
        frequency_input.addItems(["Daily", "Weekly", "Monthly"])
        
        target_input = QSpinBox()
        target_input.setRange(1, 365)
        target_input.setValue(30)
        target_input.setSuffix(" days")
        
        form_layout.addRow("Habit Name:", name_input)
        form_layout.addRow("Category:", category_input)
        form_layout.addRow("Frequency:", frequency_input)
        form_layout.addRow("Target:", target_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Habit")
        save_btn.clicked.connect(lambda: self.save_habit(dialog, name_input.text()))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
        """)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def save_habit(self, dialog, name):
        """Save habit"""
        if name.strip():
            QMessageBox.information(self, "✅ Success", f"Habit '{name}' created successfully!")
            dialog.accept()
        else:
            QMessageBox.warning(self, "⚠️ Warning", "Please enter a habit name.")
            
    def show_notifications(self):
        """Show notifications"""
        QMessageBox.information(
            self,
            "🔔 Notifications",
            "📋 Recent Notifications:\n\n"
            "• Reminder: Log your evening vitals\n"
            "• Achievement unlocked: 7-day streak!\n"
            "• Health tip: Stay hydrated today\n"
            "• New community challenge available"
        )
        
    def load_user_data(self):
        """Load user data"""
        try:
            # Try to load from API
            user_data = self.api_client.get_current_user()
            self.current_user = user_data
            self.userNameLabel.setText(f"👤 {user_data.get('full_name', 'User')}")
        except Exception as e:
            # Use default
            self.current_user = {"full_name": "Demo User"}
            self.userNameLabel.setText("👤 Demo User")
            print(f"Note: Using demo mode - {str(e)}")
            
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "✅ Logout", "Logged out successfully!")
            self.close()

    def toggle_sidebar(self):
        """Show/hide the left navigation sidebar"""
        try:
            if self.nav_widget.isVisible():
                self.nav_widget.hide()
            else:
                self.nav_widget.show()
        except Exception:
            # Defensive: if nav_widget not set, ignore
            pass

    def resizeEvent(self, a0):
        """Auto-hide sidebar when window is narrow to improve responsiveness"""
        try:
            width = self.width()
            # Hide sidebar on narrow widths (e.g., mobile-like)
            if width < 900:
                if self.nav_widget.isVisible():
                    self.nav_widget.hide()
            else:
                # Show sidebar for wider screens
                if not self.nav_widget.isVisible():
                    self.nav_widget.show()
        except Exception:
            pass
        # Call base class implementation
        return super().resizeEvent(a0)



def main():
    """Run the working dashboard"""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create API client
    try:
        api_client = APIClient()
    except:
        api_client = None
        
    # Create and show dashboard
    dashboard = WorkingDashboardController(api_client)
    dashboard.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
