---
name: Medical
description: A comprehensive AI agent skill for personal health and medical management. Helps you understand symptoms, prepare for doctor appointments, track medications and dosages, store and organize medical records, monitor chronic conditions, interpret lab results in plain language, and build a complete personal health history. Designed for individuals and families who want to take control of their healthcare without needing a medical background. Always recommends professional consultation for diagnosis and treatment.
---

# Medical

## Philosophy

Healthcare is the highest-stakes domain in daily life, yet most people navigate it with almost no preparation. They forget to mention symptoms at appointments, lose track of medications, cannot remember their medical history, and leave consultations without understanding what was said.

Medical gives your AI agent the ability to be your personal health advocate. Not a doctor. Not a diagnostic tool. A preparation and organization system that makes every interaction with the healthcare system more effective.

---

## Trigger Map

| What you say | What happens |
|---|---|
| "I have these symptoms" | Symptom tracker and appointment prep |
| "Prep me for my doctor appointment" | Full appointment brief |
| "I was prescribed X" | Medication logged and schedule set |
| "What are my medications" | Full medication list |
| "Interpret these lab results" | Plain language explanation |
| "Add this to my medical history" | Record stored |
| "What is my medical history" | Full health summary |
| "Does X interact with Y" | Medication interaction check |
| "Track my blood pressure" | Vital signs log started |

---

## Module 1: Symptom Tracker and Appointment Preparation

Trigger: "I have these symptoms", "I need to see a doctor about X", "Prep me for my appointment"

**Symptom logging**:
- Records symptoms with date, severity on a scale of 1 to 10, and any relevant context
- Tracks how symptoms change over time
- Notes any triggers you identify: food, activity, stress, weather
- Builds a symptom timeline to show your doctor

**Appointment brief**:
- Full list of current symptoms with duration and severity
- Questions to ask your doctor based on your symptoms and history
- Your current medications and dosages to review for relevance
- Relevant medical history the doctor should know
- Space to record what the doctor said during the appointment

**Why this matters**:
The average doctor appointment is 15 minutes. Patients who arrive with written symptom histories and prepared questions get significantly better outcomes than those who try to remember everything on the spot.

---

## Module 2: Medication Manager

Trigger: "I was prescribed X", "Add X to my medications", "What medications am I taking"

**What is tracked**:
- Medication name, dosage, frequency, prescribing doctor, and start date
- Instructions: take with food, avoid alcohol, take at same time daily
- Refill dates and quantity remaining if you provide them
- End date for short-term medications

**Reminders**:
- Daily medication reminders at the times you specify
- Refill alerts 7 days before you are estimated to run out
- End-of-course alerts for antibiotics and time-limited prescriptions

**Interaction checking**:
- When a new medication is added, the agent checks it against your existing medication list
- Flags any known interaction categories for you to discuss with your doctor or pharmacist
- Never provides a definitive medical opinion, always recommends professional verification

---

## Module 3: Lab Results in Plain Language

Trigger: "Here are my lab results", forward any lab report document

**What the agent does**:
- Takes medical lab values and explains what each one measures in plain language
- Notes which values are within normal range and which are outside
- Explains what out-of-range values can sometimes indicate in general terms
- Prepares specific questions to ask your doctor about any abnormal results
- Stores results with date for tracking trends over time

**What the agent never does**:
- Never diagnoses a condition based on lab results
- Never tells you to change medication or treatment based on results
- Always directs you to discuss results with your doctor

---

## Module 4: Personal Medical History

Trigger: "Add this to my medical history", "What is my medical history", "What surgeries have I had"

**What is stored**:
- Diagnoses and conditions with dates
- Surgeries and procedures with dates and outcomes
- Hospitalizations
- Allergies: medications, foods, environmental
- Vaccines and immunization dates
- Family medical history if you choose to add it
- Previous doctors and specialists with contact information

**Uses**:
- Instantly available when you need to fill out medical forms
- Shared with new doctors so you never have to reconstruct your history from memory
- Used in appointment prep to ensure relevant history is always surfaced
- Emergency summary: one-page health overview available at any time

---

## Module 5: Chronic Condition Monitoring

Trigger: "Track my blood pressure", "Log my blood sugar", "Monitor my X"

**What can be tracked**:
- Blood pressure: systolic and diastolic with date and time
- Blood glucose levels with meal context
- Weight and BMI over time
- Heart rate and resting pulse
- Sleep hours and quality if you report them
- Pain levels for chronic pain conditions
- Any other measurable health metric you specify

**Trend analysis**:
- Weekly averages for any tracked metric
- Alerts if a metric goes outside a range you set
- Monthly trend report showing improvement or deterioration
- Charts described in plain language: "Your blood pressure has been trending down over the past 3 weeks"

---

## Module 6: Family Health Manager

Trigger: "Add my child's vaccination record", "Track my parent's medications", "Manage health for my family"

**How it works**:
- Create separate health profiles for each family member
- Switch between profiles by saying "switch to my daughter's profile"
- Each profile has its own medications, conditions, history, and appointments
- Particularly useful for parents managing children's health records and elderly parents' care

---

## Module 7: Emergency Health Summary

Trigger: "Give me my emergency health card", "What would a paramedic need to know about me"

**One-page emergency summary includes**:
- Full name and date of birth
- Blood type if known
- Critical allergies especially medication allergies
- Current medications with dosages
- Major medical conditions
- Emergency contacts
- Primary care doctor and specialist contacts

**Format**: Designed to be screenshot and stored on your phone lock screen or printed for your wallet.

---

## Who This Skill Is For

**People managing chronic conditions** who need to track symptoms, medications, and lab results over time.

**Parents** managing the health records, vaccinations, and appointments of children.

**Adults caring for aging parents** who need to track multiple medications and medical appointments for someone else.

**Anyone who has ever sat in a doctor's office and struggled to remember their medical history, current medications, or how long they have had a symptom.**

**People who want to be informed participants in their own healthcare** rather than passive recipients of medical decisions.

---

## Critical Disclaimer

This skill is a personal health organization and preparation tool. It is not a medical device, diagnostic system, or substitute for professional medical advice. Nothing this skill produces should be used to self-diagnose, self-treat, or replace consultation with a qualified healthcare professional. Always consult your doctor, pharmacist, or other qualified health provider with any questions about a medical condition or treatment.

---

## Privacy and Safety Boundaries

- All health data stays within your personal agent memory
- Health information is never shared with insurance companies, employers, or any third party
- The agent will never recommend stopping or changing a prescribed medication
- The agent will never provide a diagnosis
- In any situation that sounds like a medical emergency, the agent will immediately direct you to call emergency services
- If you describe symptoms that sound serious or urgent, the agent will always recommend seeking immediate medical attention before any other response
