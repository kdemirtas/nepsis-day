# Privacy Policy for Nepsis

Last updated: 10 September 2026

Nepsis is a recovery companion app for people staying away from alcohol. It keeps your sobriety record, can read your health signals, shows you a risk estimate with its reasoning, and helps you reach your people and emergency services quickly. This policy describes what the app does with your information.

## The summary

Your data lives on your phone. The app works fully without any server: the emergency screens, the call buttons and the SMS cascade never need a network connection. While the app is in private testing with a single user, a copy of the record is mirrored to a computer owned by the developer, for backup only; no data is shared with anyone else. There are no advertisements, no analytics, and no tracking of any kind.

## What the app stores, and where

All of the following is stored on your device, in the app's private storage, and is deleted when you uninstall the app or choose "Delete everything" in Settings:

- **Your profile:** a username, a display name (no real names are required; initials are fine), your phone number, your country and city, your sex (used only to score a standard questionnaire), and your language.
- **Your recovery record:** when you last drank, each episode you log, and your answers to the intake questionnaire (which includes questions about your drinking history, past withdrawal, medications, and medical conditions such as a transplant).
- **Your companions:** the names and phone numbers of the people you choose, in the order you want them called, and whether they agreed to be contacted.
- **Your settings:** the emergency number override, your transplant team's number, and whether you allowed the app to notify your companions automatically.
- **A log of every automatic message the app sent on your behalf**, so you can always see what was sent, to whom, and when.
- **Health signals** (from a later version): heart rate, sleep, steps and workouts read from Health Connect, and any blood pressure or temperature you enter by hand.
- **Risk estimates** (from a later version): each estimate with the rules that produced it.

Android backup is disabled for this app, so no copy is placed in your Google account backup.

## What the app sends, and to whom

- **SMS messages to your companions.** Only if you turned on automatic notification in advance, only after the timer you set runs out without you placing a call, and only to the people you listed. Each message includes your display name and, if you allowed it, your location. Your companions see the message in their normal messaging app.
- **Phone calls.** When you tap a companion or the emergency number, the app places the call through your phone's dialer. Nothing else is sent.
- **The developer's mirror computer** (private testing only). Your profile, record, companions, message log and questionnaire answers are copied to a computer owned by the developer when the phone can reach it, for backup. The phone never downloads anything from it. This mirror will be replaced by a properly hosted service, with its own updated policy, before any second user is admitted.
- **The AI Companion** (from a later version). When you use the chat, the app sends the conversation together with a summary of your record, recent signals and the current risk estimate to Anthropic's Claude API, so the assistant can answer with context. Anthropic's handling of that request is governed by its own privacy policy. Nothing is sent when you are not using the chat.

Any web request reveals your device's IP address to the receiving service, as all web requests do.

## Sensitive data

This app handles health data: your alcohol history, withdrawal history, medications, medical conditions, and vital signs. It exists for exactly that purpose. This data stays on your device except as described above (the developer's backup mirror during private testing, and the AI chat when you use it). You can delete all of it at any time from Settings. The app also handles your location, only when you grant it, and only for the features that ask for it on screen with a reason: the emergency message to your companions, and, later, nearby meetings and the risk estimate.

## Permissions

- **Phone calls (CALL_PHONE):** to call a companion or the emergency number with one tap. If declined, tapping opens the dialer with the number filled in instead.
- **Send SMS (SEND_SMS):** for the automatic message to your companions. If declined, automatic notification is turned off and the app tells you so.
- **Location:** only if you choose to include your location in the emergency message, or use a location-based feature. If declined, messages are sent without it.
- **Notifications:** to show the running timer and what was sent. If declined, the timer still runs but you will not see it in the notification shade.
- **Health Connect** (later version): to read heart rate, sleep, steps and workouts. If declined, the app works without signals.
- **Exact alarms and running in the background:** so the timer keeps running after you close the app or restart the phone.

## Children

Nepsis is not directed at children and is intended for adults aged 18 and over.

## Your control

"Export" in Settings gives you a file with everything the app stores. "Delete everything" removes all of it from your device. During private testing, ask the developer to delete the mirror copy; there is nothing else outside your device to request.

## Affiliation

Nepsis is independent. It is not affiliated with Alcoholics Anonymous, any treatment provider, or any hospital. It does not provide medical care and is not a substitute for it. If you are in withdrawal, call emergency services.

## Changes

If this policy changes, the "last updated" date above will change with it.

## Contact

keremdemirtas@gmail.com
