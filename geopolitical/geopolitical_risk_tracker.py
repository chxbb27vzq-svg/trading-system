#!/usr/bin/env python3
"""
Geopolitical Risk Tracker
Tracks sanctions, political events, and their impact on markets
Based on lessons learned from Oil Sanctions analysis
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

class GeopoliticalRiskTracker:
    """
    Tracks geopolitical events and calculates their market impact
    """
    
    def __init__(self, db_path: str = "geopolitical_risks.db"):
        self.db_path = db_path
        self.init_database()
        
        # Historical sanctions patterns (from our analysis)
        self.sanctions_patterns = {
            "iran_2018": {
                "short_term_spike": 0.12,  # +12%
                "correction": -0.05,
                "long_term_premium": 0.08,
                "compliance_cost": 7.5,  # $/barrel
                "export_stop_probability": 0.05
            },
            "venezuela_2019": {
                "short_term_spike": 0.05,
                "correction": -0.02,
                "long_term_premium": 0.03,
                "compliance_cost": 10.0,
                "export_stop_probability": 0.10
            },
            "russia_2022": {
                "short_term_spike": 0.25,
                "correction": -0.10,
                "long_term_premium": 0.07,
                "compliance_cost": 32.0,  # Dallas Fed study
                "export_stop_probability": 0.05
            }
        }
    
    def init_database(self):
        """Initialize geopolitical risks database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Geopolitical events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS geopolitical_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_date DATE NOT NULL,
                event_type TEXT NOT NULL,
                description TEXT,
                affected_assets TEXT,
                severity TEXT,
                sanctions_probability REAL,
                estimated_impact REAL,
                actual_impact REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sanctions tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sanctions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sanction_date DATE NOT NULL,
                target_country TEXT NOT NULL,
                target_entity TEXT,
                sanction_type TEXT,
                affected_volume REAL,
                compliance_cost REAL,
                workaround_established BOOLEAN DEFAULT 0,
                export_stopped BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Market impact patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS impact_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                asset_class TEXT NOT NULL,
                short_term_spike REAL,
                correction REAL,
                long_term_premium REAL,
                compliance_cost REAL,
                export_stop_prob REAL,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_geopolitical_event(self, event_type: str, description: str,
                              affected_assets: List[str], severity: str,
                              sanctions_probability: float = 0.0) -> int:
        """
        Add a geopolitical event
        
        Args:
            event_type: Type of event (sanctions, conflict, policy_change, etc.)
            description: Event description
            affected_assets: List of affected assets (oil, gold, stocks, etc.)
            severity: LOW, MEDIUM, HIGH, CRITICAL
            sanctions_probability: Probability of sanctions (0-1)
        
        Returns:
            Event ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO geopolitical_events 
            (event_date, event_type, description, affected_assets, severity, sanctions_probability)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().date(),
            event_type,
            description,
            json.dumps(affected_assets),
            severity,
            sanctions_probability
        ))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return event_id
    
    def add_sanctions(self, target_country: str, target_entity: str,
                     sanction_type: str, affected_volume: float,
                     compliance_cost: float = 0.0) -> int:
        """
        Add sanctions tracking
        
        Args:
            target_country: Country being sanctioned
            target_entity: Entity being sanctioned (e.g., Rosneft, Lukoil)
            sanction_type: Type of sanctions (oil, financial, trade, etc.)
            affected_volume: Volume affected (million bpd for oil)
            compliance_cost: Estimated compliance cost ($/barrel)
        
        Returns:
            Sanctions ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sanctions 
            (sanction_date, target_country, target_entity, sanction_type, 
             affected_volume, compliance_cost)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().date(),
            target_country,
            target_entity,
            sanction_type,
            affected_volume,
            compliance_cost
        ))
        
        sanction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return sanction_id
    
    def calculate_sanctions_impact(self, sanction_id: int, 
                                   pattern_name: str = "russia_2022") -> Dict:
        """
        Calculate expected market impact based on historical patterns
        
        Args:
            sanction_id: ID of the sanctions
            pattern_name: Historical pattern to use (iran_2018, venezuela_2019, russia_2022)
        
        Returns:
            Dict with impact estimates
        """
        pattern = self.sanctions_patterns.get(pattern_name, self.sanctions_patterns["russia_2022"])
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sanctions WHERE id = ?', (sanction_id,))
        sanction = cursor.fetchone()
        conn.close()
        
        if not sanction:
            return {}
        
        affected_volume = sanction[5]  # affected_volume column
        
        # Calculate impact
        impact = {
            "short_term_price_change": pattern["short_term_spike"],
            "correction": pattern["correction"],
            "long_term_premium": pattern["long_term_premium"],
            "compliance_cost_per_barrel": pattern["compliance_cost"],
            "export_stop_probability": pattern["export_stop_probability"],
            "workaround_probability": 1 - pattern["export_stop_probability"],
            "affected_volume_mbpd": affected_volume,
            "global_supply_impact_pct": (affected_volume / 100) * 100,  # Assuming 100 mbpd global
            "pattern_used": pattern_name,
            "confidence": 0.75  # Based on historical validation
        }
        
        return impact
    
    def get_active_risks(self, days: int = 30) -> List[Dict]:
        """
        Get active geopolitical risks from last N days
        
        Args:
            days: Number of days to look back
        
        Returns:
            List of active risks
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).date()
        
        cursor.execute('''
            SELECT * FROM geopolitical_events 
            WHERE event_date >= ?
            ORDER BY severity DESC, event_date DESC
        ''', (cutoff_date,))
        
        events = cursor.fetchall()
        conn.close()
        
        risks = []
        for event in events:
            risks.append({
                "id": event[0],
                "date": event[1],
                "type": event[2],
                "description": event[3],
                "affected_assets": json.loads(event[4]) if event[4] else [],
                "severity": event[5],
                "sanctions_probability": event[6],
                "estimated_impact": event[7],
                "actual_impact": event[8]
            })
        
        return risks
    
    def generate_risk_report(self) -> str:
        """Generate comprehensive geopolitical risk report"""
        risks = self.get_active_risks(30)
        
        report = "="*70 + "\n"
        report += "GEOPOLITICAL RISK REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += "="*70 + "\n\n"
        
        if not risks:
            report += "✅ NO ACTIVE GEOPOLITICAL RISKS (Last 30 days)\n"
            return report
        
        # Group by severity
        critical = [r for r in risks if r["severity"] == "CRITICAL"]
        high = [r for r in risks if r["severity"] == "HIGH"]
        medium = [r for r in risks if r["severity"] == "MEDIUM"]
        low = [r for r in risks if r["severity"] == "LOW"]
        
        if critical:
            report += "🔴 CRITICAL RISKS:\n"
            report += "-" * 70 + "\n"
            for risk in critical:
                report += f"• {risk['date']}: {risk['description']}\n"
                report += f"  Affected: {', '.join(risk['affected_assets'])}\n"
                if risk['sanctions_probability'] > 0:
                    report += f"  Sanctions Probability: {risk['sanctions_probability']*100:.0f}%\n"
                report += "\n"
        
        if high:
            report += "🟠 HIGH RISKS:\n"
            report += "-" * 70 + "\n"
            for risk in high:
                report += f"• {risk['date']}: {risk['description']}\n"
                report += f"  Affected: {', '.join(risk['affected_assets'])}\n"
                report += "\n"
        
        if medium:
            report += "🟡 MEDIUM RISKS:\n"
            report += "-" * 70 + "\n"
            for risk in medium:
                report += f"• {risk['date']}: {risk['description']}\n"
                report += "\n"
        
        report += "="*70 + "\n"
        report += f"Total Active Risks: {len(risks)}\n"
        report += f"Critical: {len(critical)} | High: {len(high)} | Medium: {len(medium)} | Low: {len(low)}\n"
        
        return report


if __name__ == "__main__":
    # Example usage
    tracker = GeopoliticalRiskTracker()
    
    print("=== GEOPOLITICAL RISK TRACKER - DEMO ===\n")
    
    # Add Rosneft/Lukoil sanctions (current)
    print("Adding Rosneft/Lukoil sanctions...")
    sanction_id = tracker.add_sanctions(
        target_country="Russia",
        target_entity="Rosneft, Lukoil",
        sanction_type="oil_export",
        affected_volume=3.5,  # million bpd
        compliance_cost=25.0  # estimated $/barrel
    )
    print(f"✅ Sanctions added (ID: {sanction_id})\n")
    
    # Calculate impact
    print("Calculating market impact based on historical patterns...\n")
    impact = tracker.calculate_sanctions_impact(sanction_id, "russia_2022")
    
    print("EXPECTED IMPACT (Based on Russia 2022 Pattern):")
    print("-" * 70)
    print(f"Short-term price spike: +{impact['short_term_price_change']*100:.1f}%")
    print(f"Correction: {impact['correction']*100:.1f}%")
    print(f"Long-term premium: +{impact['long_term_premium']*100:.1f}%")
    print(f"Compliance cost: ${impact['compliance_cost_per_barrel']:.2f}/barrel")
    print(f"Export stop probability: {impact['export_stop_probability']*100:.0f}%")
    print(f"Workaround probability: {impact['workaround_probability']*100:.0f}%")
    print(f"Confidence: {impact['confidence']*100:.0f}%")
    print()
    
    # Add geopolitical event
    print("Adding geopolitical event...")
    event_id = tracker.add_geopolitical_event(
        event_type="sanctions",
        description="US sanctions on Rosneft & Lukoil (Oct 22, 2025)",
        affected_assets=["Brent", "WTI", "Russian Stocks"],
        severity="HIGH",
        sanctions_probability=1.0
    )
    print(f"✅ Event added (ID: {event_id})\n")
    
    # Generate report
    print(tracker.generate_risk_report())
    
    print("\n✅ GEOPOLITICAL RISK TRACKER OPERATIONAL")

