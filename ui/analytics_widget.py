"""Analytics widget for trading data"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QTableWidget, QTableWidgetItem, QComboBox, QPushButton,
    QDateEdit, QCheckBox, QTextEdit, QMessageBox, QHeaderView
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor
from models.database import TradeDatabase
from analysis.charts import ChartGenerator
from analysis.search import TradeFilter
from analysis.export import TradeExporter
from ui.modern_styles import get_colors
from datetime import datetime

class AnalyticsWidget(QWidget):
    """Advanced analytics and reporting widget"""
    
    def __init__(self, theme='dark'):
        super().__init__()
        self.theme = theme
        self.colors = get_colors(theme)
        self.db = TradeDatabase()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        
        # Filter section
        filter_group = QGroupBox("Filters")
        filter_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['text']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
            }}
        """)
        filter_layout = QHBoxLayout()
        
        # Symbol filter
        filter_layout.addWidget(QLabel("Symbol:"))
        self.symbol_combo = QComboBox()
        self.symbol_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 6px;
                color: {self.colors['text']};
            }}
        """)
        self.symbol_combo.addItem("All")
        self.symbol_combo.addItems(['USDCAD', 'EURUSD', 'XAUUSD', 'NAS100', 'US30'])
        filter_layout.addWidget(self.symbol_combo)
        
        # Result filter
        filter_layout.addWidget(QLabel("Result:"))
        self.result_combo = QComboBox()
        self.result_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 6px;
                color: {self.colors['text']};
            }}
        """)
        self.result_combo.addItems(["All", "Win", "Loss"])
        filter_layout.addWidget(self.result_combo)
        
        # A+ only
        self.aplus_checkbox = QCheckBox("A+ Setup Only")
        self.aplus_checkbox.setStyleSheet(f"color: {self.colors['text']};")
        filter_layout.addWidget(self.aplus_checkbox)
        
        # Min confirmations
        filter_layout.addWidget(QLabel("Min Confirmations:"))
        self.min_conf_combo = QComboBox()
        self.min_conf_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.colors['surface']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 6px;
                color: {self.colors['text']};
            }}
        """)
        self.min_conf_combo.addItems(["All"] + [str(i) for i in range(11)])
        filter_layout.addWidget(self.min_conf_combo)
        
        filter_layout.addStretch()
        filter_group.setLayout(filter_layout)
        main_layout.addWidget(filter_group)
        
        # Monthly stats section
        monthly_group = QGroupBox("📊 Monthly Statistics")
        monthly_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['text']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
            }}
        """)
        monthly_layout = QVBoxLayout()
        
        self.monthly_table = QTableWidget()
        self.monthly_table.setColumnCount(6)
        self.monthly_table.setHorizontalHeaderLabels([
            "Month", "Total Trades", "Wins", "Losses", "Win Rate", "A+ Setups"
        ])
        self.monthly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.monthly_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.colors['surface']};
                gridline-color: {self.colors['border']};
                border: 1px solid {self.colors['border']};
            }}
            QTableWidget::item {{
                padding: 8px;
                color: {self.colors['text']};
            }}
            QTableWidget::item:selected {{
                background-color: {self.colors['primary']};
                color: #000000;
            }}
            QHeaderView::section {{
                background-color: {self.colors['primary']};
                color: #000000;
                padding: 8px;
                font-weight: bold;
            }}
        """)
        
        monthly_layout.addWidget(self.monthly_table)
        monthly_group.setLayout(monthly_layout)
        main_layout.addWidget(monthly_group)
        
        # Confirmation effectiveness section
        conf_group = QGroupBox("✓ Confirmation Signal Effectiveness")
        conf_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['text']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
            }}
        """)
        conf_layout = QVBoxLayout()
        
        self.conf_table = QTableWidget()
        self.conf_table.setColumnCount(5)
        self.conf_table.setHorizontalHeaderLabels([
            "Signal", "Total", "Wins", "Losses", "Effectiveness"
        ])
        self.conf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.conf_table.setMinimumHeight(300)
        self.conf_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.colors['surface']};
                gridline-color: {self.colors['border']};
                border: 1px solid {self.colors['border']};
            }}
            QTableWidget::item {{
                padding: 8px;
                color: {self.colors['text']};
            }}
            QTableWidget::item:selected {{
                background-color: {self.colors['primary']};
                color: #000000;
            }}
            QHeaderView::section {{
                background-color: {self.colors['primary']};
                color: #000000;
                padding: 8px;
                font-weight: bold;
            }}
        """)
        
        conf_layout.addWidget(self.conf_table)
        conf_group.setLayout(conf_layout)
        main_layout.addWidget(conf_group)
        
        # Export section
        export_group = QGroupBox("📥 Export")
        export_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['text']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
            }}
        """)
        export_layout = QHBoxLayout()
        
        csv_btn = QPushButton("📊 Export to CSV")
        csv_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['success_light']};
            }}
        """)
        csv_btn.clicked.connect(self.export_csv)
        export_layout.addWidget(csv_btn)
        
        json_btn = QPushButton("📋 Export to JSON")
        json_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['info']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['info_light']};
            }}
        """)
        json_btn.clicked.connect(self.export_json)
        export_layout.addWidget(json_btn)
        
        export_layout.addStretch()
        export_group.setLayout(export_layout)
        main_layout.addWidget(export_group)
        
        self.setLayout(main_layout)
        self.load_data()
    
    def load_data(self):
        """Load and display analytics data"""
        trades = self.db.get_all_trades()
        
        # Load monthly stats
        monthly_stats = ChartGenerator.get_monthly_stats(trades)
        self.monthly_table.setRowCount(0)
        
        for row, (month_key, stats) in enumerate(monthly_stats.items()):
            self.monthly_table.insertRow(row)
            self.monthly_table.setItem(row, 0, QTableWidgetItem(stats['name']))
            self.monthly_table.setItem(row, 1, QTableWidgetItem(str(stats['total'])))
            self.monthly_table.setItem(row, 2, QTableWidgetItem(str(stats['wins'])))
            self.monthly_table.setItem(row, 3, QTableWidgetItem(str(stats['losses'])))
            self.monthly_table.setItem(row, 4, QTableWidgetItem(f"{stats['win_rate']:.1f}%"))
            self.monthly_table.setItem(row, 5, QTableWidgetItem(str(stats['aplus'])))
        
        # Load confirmation effectiveness
        conf_stats = ChartGenerator.get_confirmation_effectiveness(trades)
        self.conf_table.setRowCount(0)
        
        sorted_confs = sorted(conf_stats.items(), 
                            key=lambda x: x[1]['effectiveness'], 
                            reverse=True)
        
        for row, (conf_key, stats) in enumerate(sorted_confs):
            self.conf_table.insertRow(row)
            
            signal_item = QTableWidgetItem(stats['label'])
            signal_item.setToolTip(stats['label'])
            self.conf_table.setItem(row, 0, signal_item)
            
            self.conf_table.setItem(row, 1, QTableWidgetItem(str(stats['total'])))
            self.conf_table.setItem(row, 2, QTableWidgetItem(str(stats['wins'])))
            self.conf_table.setItem(row, 3, QTableWidgetItem(str(stats['losses'])))
            
            eff_item = QTableWidgetItem(f"{stats['effectiveness']:.1f}%")
            self.conf_table.setItem(row, 4, eff_item)
        
        self.conf_table.resizeRowsToContents()
    
    def export_csv(self):
        """Export filtered trades to CSV"""
        trades = self.db.get_all_trades()
        filepath = TradeExporter.export_to_csv(trades)
        QMessageBox.information(self, "Success", f"Exported to {filepath}")
    
    def export_json(self):
        """Export filtered trades to JSON"""
        trades = self.db.get_all_trades()
        filepath = TradeExporter.export_to_json(trades)
        QMessageBox.information(self, "Success", f"Exported to {filepath}")
    
    def set_theme(self, theme: str):
        """Update theme"""
        self.theme = theme
        self.colors = get_colors(theme)
        self.init_ui()
