<?php
/* Heleospace contact form handler for cPanel (PHP 7.4+).
   Sends each message to hello@heleo.space with PHP mail().
   Spam protection: a human-check sum, a hidden honeypot field, a minimum fill time,
   and a limit of 5 messages per visitor per hour. */

$TO        = 'hello@heleo.space';
$BCC       = '';   // blind copy of every message; set '' to turn off
$FROM      = 'hello@heleo.space';   // must be an address on this domain for good delivery
$THANKS    = '/contact/thanks/';
$BACK      = '/contact/';
$MAX_PER_HOUR = 5;

session_start();

function back($code) {
    global $BACK;
    header('Location: ' . $BACK . '?error=' . urlencode($code) . '#write', true, 303);
    exit;
}
function clean($s, $max) {
    $s = trim((string)$s);
    $s = str_replace(["\r", "\0"], '', $s);
    return function_exists('mb_substr') ? mb_substr($s, 0, $max) : substr($s, 0, $max);
}
function one_line($s) { return trim(preg_replace('/[\r\n]+/', ' ', $s)); }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: ' . $BACK, true, 303); exit; }

// 1. Honeypot: real people never fill this hidden field.
if (!empty($_POST['hx_trap_9'])) { header('Location: ' . $THANKS, true, 303); exit; }

// 2. Human check: the sum shown on the form.
$answer = isset($_SESSION['hc_answer']) ? (int)$_SESSION['hc_answer'] : null;
$issued = isset($_SESSION['hc_issued']) ? (int)$_SESSION['hc_issued'] : 0;
unset($_SESSION['hc_answer']);                       // one use only
if ($answer === null || trim($_POST['human'] ?? '') === '' || (int)$_POST['human'] !== $answer) back('check');

// 3. Too fast to be human (under 3 seconds) or too old (over 2 hours).
$age = time() - $issued;
if ($age < 3 || $age > 7200) back('check');

// 4. Rate limit per session.
$now = time();
$_SESSION['hc_sent'] = array_values(array_filter($_SESSION['hc_sent'] ?? [], function ($t) use ($now) { return $now - $t < 3600; }));
if (count($_SESSION['hc_sent']) >= $MAX_PER_HOUR) back('limit');

// 5. Validate fields.
$name    = one_line(clean($_POST['name'] ?? '', 120));
$email   = one_line(clean($_POST['email'] ?? '', 200));
$org     = one_line(clean($_POST['organisation'] ?? '', 160));
$topic   = one_line(clean($_POST['topic'] ?? '', 60));
$message = clean($_POST['message'] ?? '', 5000);
$topics  = ['Research collaboration', 'Partnership', 'Careers', 'Investor relations', 'Press', 'Something else'];
if (!in_array($topic, $topics, true)) $topic = 'Something else';
if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) back('fields');

// 6. Send.
$subject = '[heleo.space] ' . $topic . ' — ' . $name . ($org !== '' ? ' (' . $org . ')' : '');
$body  = "New message from the heleo.space contact form\n\n";
$body .= "Name:         $name\n";
$body .= "Email:        $email\n";
$body .= "Organisation: " . ($org !== '' ? $org : '-') . "\n";
$body .= "Topic:        $topic\n";
$body .= "Sent:         " . gmdate('Y-m-d H:i') . " UTC\n\n";
$body .= "Message:\n" . $message . "\n";

$headers  = "From: Heleospace website <$FROM>\r\n";
$headers .= "Reply-To: " . $email . "\r\n";
if ($BCC !== '') $headers .= "Bcc: " . $BCC . "\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";

$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$ok = @mail($TO, $encodedSubject, $body, $headers, '-f' . $FROM);
if (!$ok) back('send');

$_SESSION['hc_sent'][] = $now;
header('Location: ' . $THANKS, true, 303);
exit;
