<?php
header('Content-Type: application/json');

// Only allow POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

// Read JSON body
$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid request body']);
    exit;
}

$name         = trim($input['name'] ?? '');
$email        = trim($input['email'] ?? '');
$organisation = trim($input['organisation'] ?? '');
$subject      = trim($input['subject'] ?? '');
$message      = trim($input['message'] ?? '');

// Validate required fields
if ($name === '' || $email === '' || $subject === '' || $message === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required fields']);
    exit;
}

// Validate email
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid email address']);
    exit;
}

// Map subject keys to labels
$subjectLabels = [
    'collaboration' => 'Collaboration & Partnerships',
    'research'      => 'Research Inquiry',
    'training'      => 'Training & Workshops',
    'media'         => 'Media & Press',
    'other'         => 'Other',
];
$subjectLabel = $subjectLabels[$subject] ?? $subject;

// Build email
$to = 'eipcm@eipcm.org';
$mailSubject = '[EIPCM Contact] ' . $subjectLabel;

$body  = "Name: $name\n";
$body .= "Email: $email\n";
if ($organisation !== '') {
    $body .= "Organisation: $organisation\n";
}
$body .= "Subject: $subjectLabel\n\n";
$body .= "Message:\n$message\n";

$headers  = "From: EIPCM Website <noreply@eipcm.org>\r\n";
$headers .= "Reply-To: $name <$email>\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

// Send
if (mail($to, $mailSubject, $body, $headers)) {
    echo json_encode(['success' => true]);
} else {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to send email']);
}
