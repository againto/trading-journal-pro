"""Form for entering new trades with validation"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QCheckBox, QPushButton, QTabWidget, QGroupBox, QRadioButton,
    QButtonGroup, QTextEdit, QMessageBox, QDateEdit, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont
from models.trade import Trade
from models.database import TradeDatabase
from analysis.validators import TradeValidator
from ui.modern_styles import get_colors
from ui.styles import SYMBOLS, DIRECTIONS
from ui.emotional_mistakes_widget import EmotionalMistakesWidget
from ui.technical_mistakes_widget import TechnicalMistakesWidget
import logging

logger = logging.getLogger(__name__)

class TradeForm(QWidget):
    """Form for entering new trades"""
    
    trade_saved = pyqtSignal()
    
    def __init__(self, theme='dark'):
        super().__init__()
        self.theme = theme
        self.colors = get_colors(theme)
        self.db = TradeDatabase()
        self.validator = TradeValidator()
        self.init_ui()
        logger.info("Trade form initialized")
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel("📝 New Trade")
        title_font = QFont("Segoe UI", 14)
        title_font.setWeight(QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {self.colors['primary']};")
        main_layout.addWidget(title)
        
        # Top section - Symbol and Date
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        # Symbol dropdown
        top_layout.addWidget(QLabel("Symbol:"))
        self.symbol_combo = QComboBox()
        self.symbol_combo.setStyleSheet(self._get_combo_style())
        self.symbol_combo.addItems(SYMBOLS)
        top_layout.addWidget(self.symbol_combo, 1)
        
        # Date picker
        top_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet(self._get_input_style())
        top_layout.addWidget(self.date_edit, 1)
        
        # A+ Setup checkbox
        self.aplus_checkbox = QCheckBox("⭐ A+ Setup")
        self.aplus_checkbox.setStyleSheet(f"color: {self.colors['text']};")
        top_layout.addWidget(self.aplus_checkbox)
        
        main_layout.addLayout(top_layout)
        
        # Tab widget for different sections
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabBar::tab {{
                background-color: {self.colors['bg_secondary']};
                border: none;
                padding: 10px 20px;
                margin-right: 4px;
                font-size: 11px;
                font-weight: 600;
                color: {self.colors['text_secondary']};
                border-radius: 6px 6px 0px 0px;
            }}
            QTabBar::tab:hover {{
                background-color: {self.colors['bg_tertiary']};
            }}
            QTabBar::tab:selected {{
                background-color: {self.colors['surface']};
                color: {self.colors['primary']};
                border-bottom: 3px solid {self.colors['primary']};
                font-weight: 700;
            }}
        """)
        
        # Confirmation Tab
        self.tabs.addTab(self.create_confirmation_tab(), "✓ Confirmations")
        
        # Time Frame Confluence Tab
        self.tabs.addTab(self.create_timeframe_tab(), "📊 Confluence")
        
        # Result Tab (Win/Loss)
        self.tabs.addTab(self.create_result_tab(), "📈 Result")
        
        # Emotional Mistakes Tab
        self.emotional_widget = EmotionalMistakesWidget(theme=self.theme)
        self.tabs.addTab(self.emotional_widget, "⚠️ Emotional")

        # Technical Mistakes Tab
        self.technical_widget = TechnicalMistakesWidget(theme=self.theme)
        self.tabs.addTab(self.technical_widget, "⚠️ Technical")
        
        main_layout.addWidget(self.tabs)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Save button
        save_btn = QPushButton("💾 Save Trade")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['success_light']};
            }}
        """)
        save_btn.clicked.connect(self.save_trade)
        button_layout.addWidget(save_btn)
        
        # Reset button
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['warning']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['warning_light']};
            }}
        """)
        reset_btn.clicked.connect(self.reset_form)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def _get_combo_style(self):
        """Get combobox stylesheet"""
        return f"""
            QComboBox {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 8px;
                color: {self.colors['text']};
                font-size: 11px;
            }}
            QComboBox:focus {{
                border: 2px solid {self.colors['primary']};
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.colors['surface']};
                color: {self.colors['text']};
                selection-background-color: {self.colors['primary']};
            }}
        """
    
    def _get_input_style(self):
        """Get input field stylesheet"""
        return f"""
            QDateEdit {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 8px;
                color: {self.colors['text']};
                font-size: 11px;
            }}
            QDateEdit:focus {{
                border: 2px solid {self.colors['primary']};
            }}
        """
    
    def create_confirmation_tab(self) -> QWidget:
        """Create the confirmation criteria tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        confirmations = [
            ('higher_timeframe_trend', 'Higher Time Frame Trend Aligned'),
            ('three_timeframe_aligned', '3 Time Frame Aligned'),
            ('four_timeframe_aligned', '4 Time Frame Aligned'),
            ('daily_low_taken', 'Daily Low Taken'),
            ('daily_high_taken', 'Daily High Taken'),
            ('daily_swing_low_high', 'Daily Swing Low/High Taken'),
            ('premium_discount_prices', 'From Premium and Discount Prices'),
            ('reversing_from_push', 'Reversing From Last Push'),
            ('imb_inverted_4h', 'Imb Getting Inverted 4H'),
            ('tapping_imb_4h', 'Tapping Into Imb 4H'),
        ]
        
        self.confirmation_buttons = {}
        
        for attr_name, label_text in confirmations:
            group_box = QGroupBox(label_text)
            group_box.setStyleSheet(f"""
                QGroupBox {{
                    color: {self.colors['text']};
                    border: 1px solid {self.colors['border']};
                    border-radius: 6px;
                    margin-top: 8px;
                    padding-top: 8px;
                    font-size: 10px;
                }}
            """)
            h_layout = QHBoxLayout()
            
            button_group = QButtonGroup()
            
            yes_btn = QRadioButton("Yes")
            yes_btn.setStyleSheet(f"color: {self.colors['text']};")
            no_btn = QRadioButton("No")
            no_btn.setStyleSheet(f"color: {self.colors['text']};")
            no_btn.setChecked(True)
            
            button_group.addButton(yes_btn, 1)
            button_group.addButton(no_btn, 0)
            
            h_layout.addWidget(yes_btn)
            h_layout.addWidget(no_btn)
            h_layout.addStretch()
            
            group_box.setLayout(h_layout)
            layout.addWidget(group_box)
            
            self.confirmation_buttons[attr_name] = (button_group, yes_btn, no_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_timeframe_tab(self) -> QWidget:
        """Create the time frame confluence tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        timeframes = [
            ('daily_confluence', 'Daily'),
            ('weekly_confluence', 'Weekly'),
            ('four_hour_confluence', '4 Hour'),
            ('one_hour_confluence', '1 Hour'),
            ('fifteen_min_confluence', '15 Min'),
            ('five_min_confluence', '5 Min'),
        ]
        
        self.timeframe_buttons = {}
        
        for attr_name, label_text in timeframes:
            group_box = QGroupBox(label_text)
            group_box.setStyleSheet(f"""
                QGroupBox {{
                    color: {self.colors['text']};
                    border: 1px solid {self.colors['border']};
                    border-radius: 6px;
                    margin-top: 8px;
                    padding-top: 8px;
                    font-size: 10px;
                }}
            """)
            h_layout = QHBoxLayout()
            
            button_group = QButtonGroup()
            
            yes_btn = QRadioButton("Yes")
            yes_btn.setStyleSheet(f"color: {self.colors['text']};")
            no_btn = QRadioButton("No")
            no_btn.setStyleSheet(f"color: {self.colors['text']};")
            no_btn.setChecked(True)
            
            button_group.addButton(yes_btn, 1)
            button_group.addButton(no_btn, 0)
            
            h_layout.addWidget(yes_btn)
            h_layout.addWidget(no_btn)
            h_layout.addStretch()
            
            group_box.setLayout(h_layout)
            layout.addWidget(group_box)
            
            self.timeframe_buttons[attr_name] = (button_group, yes_btn, no_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_result_tab(self) -> QWidget:
        """Create the result (Win/Loss) tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Result selection
        result_group = QGroupBox("Trade Result")
        result_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['text']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
            }}
        """)
        result_layout = QHBoxLayout()
        
        self.result_group = QButtonGroup()
        
        win_btn = QRadioButton("✓ Win")
        loss_btn = QRadioButton("✗ Loss")
        
        self.result_group.addButton(win_btn, 1)
        self.result_group.addButton(loss_btn, 0)
        
        # Style buttons
        win_btn.setStyleSheet(f"""
            QRadioButton {{
                color: {self.colors['success']};
                font-weight: bold;
                font-size: 12px;
            }}
        """)
        
        loss_btn.setStyleSheet(f"""
            QRadioButton {{
                color: {self.colors['danger']};
                font-weight: bold;
                font-size: 12px;
            }}
        """)
        
        result_layout.addWidget(win_btn)
        result_layout.addWidget(loss_btn)
        result_layout.addStretch()
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # Direction selection
        direction_group = QGroupBox("Trade Direction")
        direction_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['text']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
            }}
        """)
        direction_layout = QHBoxLayout()
        
        direction_layout.addWidget(QLabel("Direction:"))
        self.direction_combo = QComboBox()
        self.direction_combo.setStyleSheet(self._get_combo_style())
        self.direction_combo.addItem("Select Direction")
        self.direction_combo.addItems(DIRECTIONS)
        direction_layout.addWidget(self.direction_combo)
        direction_layout.addStretch()
        direction_group.setLayout(direction_layout)
        layout.addWidget(direction_group)
        
        # Risk/Reward section
        rr_group = QGroupBox("Price Levels")
        rr_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['text']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
            }}
        """)
        rr_layout = QVBoxLayout()
        
        # Entry Price
        entry_layout = QHBoxLayout()
        entry_layout.addWidget(QLabel("Entry:"))
        self.entry_price = QDoubleSpinBox()
        self.entry_price.setStyleSheet(self._get_input_style())
        self.entry_price.setMaximum(999999.99)
        self.entry_price.setDecimals(5)
        entry_layout.addWidget(self.entry_price)
        entry_layout.addStretch()
        rr_layout.addLayout(entry_layout)
        
        # Stop Loss
        sl_layout = QHBoxLayout()
        sl_layout.addWidget(QLabel("SL:"))
        self.stop_loss = QDoubleSpinBox()
        self.stop_loss.setStyleSheet(self._get_input_style())
        self.stop_loss.setMaximum(999999.99)
        self.stop_loss.setDecimals(5)
        sl_layout.addWidget(self.stop_loss)
        sl_layout.addStretch()
        rr_layout.addLayout(sl_layout)
        
        # Take Profit
        tp_layout = QHBoxLayout()
        tp_layout.addWidget(QLabel("TP:"))
        self.take_profit = QDoubleSpinBox()
        self.take_profit.setStyleSheet(self._get_input_style())
        self.take_profit.setMaximum(999999.99)
        self.take_profit.setDecimals(5)
        tp_layout.addWidget(self.take_profit)
        tp_layout.addStretch()
        rr_layout.addLayout(tp_layout)
        
        rr_group.setLayout(rr_layout)
        layout.addWidget(rr_group)
        
        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_text = QTextEdit()
        self.notes_text.setMaximumHeight(80)
        self.notes_text.setStyleSheet(self._get_input_style())
        self.notes_text.setPlaceholderText("Add any additional notes...")
        layout.addWidget(self.notes_text)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def save_trade(self):
        """Save the trade to database with validation"""
        try:
            # Validate direction selection
            if self.direction_combo.currentIndex() == 0:
                QMessageBox.warning(self, "Validation Error", "Please select a trade direction")
                return
            
            # Validate result selection
            if self.result_group.checkedId() == -1:
                QMessageBox.warning(self, "Validation Error", "Please select Win or Loss")
                return
            
            # Get confirmation responses
            confirmation_data = {}
            for attr_name, (button_group, yes_btn, no_btn) in self.confirmation_buttons.items():
                confirmation_data[attr_name] = "Yes" if yes_btn.isChecked() else "No"
            
            # Get timeframe responses
            timeframe_data = {}
            for attr_name, (button_group, yes_btn, no_btn) in self.timeframe_buttons.items():
                timeframe_data[attr_name] = "Yes" if yes_btn.isChecked() else "No"
            
            # Create trade object
            trade = Trade(
                symbol=self.symbol_combo.currentText(),
                date=self.date_edit.date().toString("yyyy-MM-dd"),
                a_plus_setup=self.aplus_checkbox.isChecked(),
                direction=self.direction_combo.currentText(),
                entry_price=self.entry_price.value(),
                stop_loss=self.stop_loss.value(),
                take_profit=self.take_profit.value(),
                result="Win" if self.result_group.checkedId() == 1 else "Loss",
                emotional_mistakes=str(self.emotional_widget.get_selected_mistakes()),
                technical_mistakes=str(self.technical_widget.get_selected_mistakes()),
                notes=self.notes_text.toPlainText(),
                **confirmation_data,
                **timeframe_data
            )
            
            # Validate trade
            is_valid, error_msg = self.validator.validate_trade(trade)
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", f"Invalid trade data:\n{error_msg}")
                return
            
            # Save to database
            trade_id = self.db.add_trade(trade)
            
            # Calculate and display signal quality
            signal_quality = trade.get_signal_quality_score()
            rr_ratio = trade.calculate_risk_reward_ratio()
            
            # Show success message
            message = f"""✓ Trade #{trade_id} saved!

Signal Quality: {signal_quality:.1f}/100
Risk:Reward: 1:{rr_ratio:.2f}
Confirmations: {trade.count_confirmations()}/10
Confluence: {trade.count_confluence()}/6
"""
            QMessageBox.information(self, "Success", message)
            logger.info(f"Trade {trade_id} saved - Quality: {signal_quality:.1f}")
            
            # Emit signal
            self.trade_saved.emit()
            
            # Reset form
            self.reset_form()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save trade: {str(e)}")
            logger.error(f"Error saving trade: {e}")
    
    def reset_form(self):
        """Reset form to default values"""
        try:
            self.symbol_combo.setCurrentIndex(0)
            self.date_edit.setDate(QDate.currentDate())
            self.aplus_checkbox.setChecked(False)
            self.notes_text.clear()
            self.direction_combo.setCurrentIndex(0)
            self.entry_price.setValue(0)
            self.stop_loss.setValue(0)
            self.take_profit.setValue(0)
            self.emotional_widget.clear_selection()
            self.technical_widget.clear_selection()
            
            # Reset all radio buttons to "No"
            for _, (button_group, yes_btn, no_btn) in self.confirmation_buttons.items():
                no_btn.setChecked(True)
            
            for _, (button_group, yes_btn, no_btn) in self.timeframe_buttons.items():
                no_btn.setChecked(True)
            
            logger.info("Form reset")
        except Exception as e:
            logger.error(f"Error resetting form: {e}")
    
    def set_theme(self, theme: str):
        """Update theme"""
        self.theme = theme
        self.colors = get_colors(theme)
        self.init_ui()
