#!/usr/bin/perl -w

#
# Addon for smbldap-tools: Change password via Web
#
# Distribution under the same conditions as smbldap-tools
#
# (c) 2009, Gerrit Beine <gerrit.beine@gmx.de>
#

use strict;
use CGI;

use lib "/usr/sbin";
use smbldap_tools;

use Crypt::SmbHash;
use Digest::MD5 qw(md5);
use Digest::SHA1 qw(sha1);
use MIME::Base64 qw(encode_base64);

my $query = new CGI();
my @parameter = $query->param();

if ( $#parameter == 3 ) {
	change_password($query);
} else {
	show_form($query);
}

exit;

sub show_form($) {
	my $response = shift;
	print $response->header(),
		$response->start_html('Change Password'),
		$response->h1('Change Password'),
		$response->start_form(),
		"Username: ",
		$response->textfield('username', '', 50, 80),
		$response->p(),
		"Old password: ",
		$response->password_field('oldpassword', '*****', 50, 80),
		$response->p(),
		"New password: ",
		$response->password_field('newpassword', '*****', 50, 80),
		$response->p(),
		"Verify new password: ",
		$response->password_field('verifypassword', '*****', 50, 80),
		$response->p(),
		$response->submit(),
		$response->end_form(),
		$response->end_html();
}

sub show_response($$) {
	my $response = shift;
	my $message = shift;
	print $response->header(), $message;

}

sub change_password($) {
	my $request = shift;

	my $username = $request->param('username');
	my $oldpassword = $request->param('oldpassword');
	my $newpassword = $request->param('newpassword');
	my $verifypassword = $request->param('verifypassword');

	if ( $newpassword ne $verifypassword ) {
		show_response($request, "Error: new password does not match verification password.");
		exit;
	}

		$config{masterDN} = "uid=$username,$config{usersdn}";
	$config{masterPw} = "$oldpassword";
	my $ldap_master = connect_ldap_master();
	my $dn = $config{masterDN};
	if ( ! is_user_valid($username, $dn, $oldpassword) ) {
		show_response($request, "Error: authentication failure.");
		exit;
	}

	my $samba = is_samba_user($username);

	if ($samba) {
		my ($sambaLMPassword, $sambaNTPassword) = ntlmgen($newpassword);
		my @mods = (
			'sambaLMPassword' => $sambaLMPassword,
			'sambaNTPassword' => $sambaNTPassword,
			'sambaPwdLastSet' => time()
		);
		my $modify = $ldap_master->modify( $dn, 'replace' => { @mods } );
		if ( $modify->code ) {
			show_response($request, "Error: failed changing Samba password.\nReason: " . $modify->error );
			exit;
		}
	}

	my $hash_password = make_hash($newpassword, $config{hash_encrypt}, $config{crypt_salt_format});
	my $shadowLastChange = int(time()/86400);

	my @mods = (
		'userPassword' => $hash_password,
		'shadowLastChange' => $shadowLastChange
	);
	my $modify = $ldap_master->modify( $dn, 'replace' => { @mods } );
	if ( $modify->code ) {
		show_response($request, "Error: failed changing Unix password.\nReason: " . $modify->error );
			exit;
	}

	if ( $samba ) {	
		show_response($request, "Success: changed Samba and Unix password" );
	} else {
		show_response($request, "Success: changed Unix password" );
	}
}

# Generates hash to be one of the following RFC 2307 schemes:
# CRYPT,  MD5,  SMD5,  SHA, SSHA,  and  CLEARTEXT
# SSHA is default
# '%s' is a default crypt_salt_format
# A substitute for slappasswd tool
sub make_hash
{
	my $hash_encrypt;
	my $crypt_salt_format;

	my $clear_pass=$_[0] or return undef;
	$hash_encrypt='{' . $_[1] . '}' or $hash_encrypt = "{SSHA}";
	$crypt_salt_format=$_[2] or $crypt_salt_format = '%s';

	my $hash_pass;
	if ($hash_encrypt eq "{CRYPT}" && defined($crypt_salt_format)) {
		# Generate CRYPT hash
		# for unix md5crypt $crypt_salt_format = '$1$%.8s'
		my $salt = sprintf($crypt_salt_format,make_salt());
		$hash_pass = "{CRYPT}" . crypt($clear_pass,$salt);

	} elsif ($hash_encrypt eq "{MD5}") {
		# Generate MD5 hash
		$hash_pass = "{MD5}" . encode_base64( md5($clear_pass),'' );

	} elsif ($hash_encrypt eq "{SMD5}") {
		# Generate SMD5 hash (MD5 with salt)
		my $salt = make_salt(4);
		$hash_pass = "{SMD5}" . encode_base64( md5($clear_pass . $salt) . $salt,'');

	} elsif ($hash_encrypt eq "{SHA}") {
		# Generate SHA1 hash
		$hash_pass = "{SHA}" . encode_base64( sha1($clear_pass),'' );

	} elsif ($hash_encrypt eq "{SSHA}") {
		# Generate SSHA hash (SHA1 with salt)
		my $salt = make_salt(4);
		$hash_pass = "{SSHA}" . encode_base64( sha1($clear_pass . $salt) . $salt,'' );

	} elsif ($hash_encrypt eq "{CLEARTEXT}") {
		$hash_pass=$clear_pass;

	} else {
		$hash_pass=undef;
	}
	return $hash_pass;
}

# Generates salt
# Similar to Crypt::Salt module from CPAN
sub make_salt
{
	my $length=32;
	$length = $_[0] if exists($_[0]);

	my @tab = ('.', '/', 0..9, 'A'..'Z', 'a'..'z');
	return join "",@tab[map {rand 64} (1..$length)];
}

