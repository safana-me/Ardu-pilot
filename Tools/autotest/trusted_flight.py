'''
Validate Trusted Flight in SITL

AP_FLAKE8_CLEAN
'''

from __future__ import print_function
import os
import shutil

from enum import Enum

from arducopter import AutoTestCopter


class TokenNameMappings(str, Enum):
    valid_token = 'valid'
    invalid_token = 'invalid'
    token_with_invalid_base64 = 'invalid_base64'
    token_with_invalid_json = 'invalid_json'
    token_without_payload = 'no_payload'
    token_without_signature = 'no_signature'
    token_without_typ = 'missing_typ'
    token_with_invalid_typ = 'invalid_typ'
    token_without_alg = 'missing_alg'
    token_with_invalid_alg = 'invalid_alg'
    token_without_iss = 'missing_iss'
    token_with_invalid_iss = 'invalid_iss'
    token_without_iat = 'missing_iat'
    token_with_invalid_iat = 'invalid_iat'
    token_with_future_iat = 'iat_in_future'
    token_without_nbf = 'missing_nbf'
    token_with_invalid_nbf = 'invalid_nbf'
    token_with_future_nbf = 'nbf_in_future'
    token_without_exp = 'missing_exp'
    token_with_invalid_exp = 'invalid_exp'
    token_with_past_exp = 'exp_in_past'


class AutoTestTrustedFlight(AutoTestCopter):

    def __del__(self):
        # cleanup test tokens and keys
        shutil.rmtree(self._get_trusted_flight_test_artifacts_directory)
        super(AutoTestTrustedFlight, self).__del__()

    @property
    def _get_trusted_flight_test_artifacts_directory(self):
        return "build/trusted_flight_artifacts/autotest/"

    @property
    def _get_trusted_flight_storage_directory(self):
        os.makedirs('trusted_flight', exist_ok=True)
        return 'trusted_flight/'

    def arming_fail(self, fail_msg, token_file=None, force=False):
        # cleanup any artifacts from previous runs
        shutil.rmtree(self._get_trusted_flight_storage_directory)

        if token_file is not None:
            # copy trusted flight artifact
            shutil.copy(f'{self._get_trusted_flight_test_artifacts_directory}/{token_file}',
                        f'{self._get_trusted_flight_storage_directory}/token')

        self.context_push()
        self.wait_ready_to_arm()
        self.assert_arm_failure(f'TrustedFlight: {fail_msg}', force=force)
        self.context_pop()

    def arming_successful(self, token_file):
        # cleanup any artifacts from previous runs
        shutil.rmtree(self._get_trusted_flight_storage_directory)

        # copy trusted flight artifact
        shutil.copy(f'{self._get_trusted_flight_test_artifacts_directory}/{token_file}',
                    f'{self._get_trusted_flight_storage_directory}/token')

        self.context_push()
        try:
            self.wait_ready_to_arm()
            self.arm_vehicle()
        except Exception as e:
            self.print_exception_caught(e)
            raise
        finally:
            self.disarm_vehicle(force=True)
            self.context_pop()

    def MissingToken(self):
        '''Token is not provided'''
        self.arming_fail('Unable to read token')

    def TokenWithInvalidBase64(self):
        '''Token with invalid base64 encoding'''
        self.arming_fail('Invalid token format', token_file=TokenNameMappings.token_with_invalid_base64)

    def TokenWithInvalidJson(self):
        '''Token with invalid json'''
        self.arming_fail('Invalid token format', token_file=TokenNameMappings.token_with_invalid_json)

    def TokenWithoutPayload(self):
        '''Token without payload'''
        self.arming_fail('Invalid token format', token_file=TokenNameMappings.token_without_payload)

    def TokenWithoutSignature(self):
        '''Token without signature'''
        self.arming_fail('Invalid token format', token_file=TokenNameMappings.token_without_signature)

    def TokenWithoutType(self):
        '''Token without typ claim in header'''
        self.arming_fail('Invalid token type', token_file=TokenNameMappings.token_without_typ)

    def TokenWithInvalidType(self):
        '''Token with invalid typ claim in header'''
        self.arming_fail('Invalid token type', token_file=TokenNameMappings.token_with_invalid_typ)

    def TokenWithoutAlgorithm(self):
        '''Token without alg claim in header'''
        self.arming_fail('Invalid token algorithm', token_file=TokenNameMappings.token_without_alg)

    def TokenWithInvalidAlgorithm(self):
        '''Token with invalid alg claim in header'''
        self.arming_fail('Invalid token algorithm', token_file=TokenNameMappings.token_with_invalid_alg)

    def TokenWithoutIssuer(self):
        '''Token without iss claim in payload'''
        self.arming_fail('Invalid token issuer', token_file=TokenNameMappings.token_without_iss)

    def TokenWithInvalidIssuer(self):
        '''Token with invalid iss claim in payload'''
        self.arming_fail('Invalid token issuer', token_file=TokenNameMappings.token_with_invalid_iss)

    def TokenWithoutIat(self):
        '''Token without iat claim in payload'''
        self.arming_fail('Invalid token iat claim', token_file=TokenNameMappings.token_without_iat)

    def TokenWithInvalidIat(self):
        '''Token with invalid iat claim in payload'''
        self.arming_fail('Invalid token iat claim', token_file=TokenNameMappings.token_with_invalid_iat)

    def TokenWithIatInFuture(self):
        '''Token with issuance time in future'''
        self.arming_fail('Invalid token iat claim', token_file=TokenNameMappings.token_with_future_iat)

    def TokenWithoutNbf(self):
        '''Token without nbf claim in payload'''
        self.arming_successful(TokenNameMappings.token_without_nbf)

    def TokenWithInvalidNbf(self):
        '''Token with invalid nbf claim in payload'''
        self.arming_fail('Invalid token nbf claim', token_file=TokenNameMappings.token_with_invalid_nbf)

    def TokenWithNbfInFuture(self):
        '''Token with notBefore in future'''
        self.arming_fail('Invalid token nbf claim', token_file=TokenNameMappings.token_with_future_nbf)

    def TokenWithoutExp(self):
        '''Token without exp claim in payload'''
        self.arming_fail('Invalid token exp claim', token_file=TokenNameMappings.token_without_exp)

    def TokenWithInvalidExp(self):
        '''Token with invalid exp claim in payload'''
        self.arming_fail('Invalid token exp claim', token_file=TokenNameMappings.token_with_invalid_exp)

    def TokenWithExpInPast(self):
        '''Token with expiration in past'''
        self.arming_fail('Invalid token exp claim', token_file=TokenNameMappings.token_with_past_exp)

    def TokenSignedWithDifferentKey(self):
        '''Token signed with another keypair'''
        self.arming_fail('Invalid token signature', token_file=TokenNameMappings.invalid_token)

    def InvalidSignedWithDifferentKeyForceArm(self):
        '''Force arm with token signed with another keypair'''
        self.arming_fail('Invalid token signature', token_file=TokenNameMappings.invalid_token, force=True)

    def ValidToken(self):
        '''Vaild token'''
        self.arming_successful(TokenNameMappings.valid_token)

    def tests(self):
        return [
            self.MissingToken,
            self.TokenWithInvalidBase64,
            self.TokenWithInvalidJson,
            self.TokenWithoutPayload,
            self.TokenWithoutSignature,
            self.TokenWithoutType,
            self.TokenWithInvalidType,
            self.TokenWithoutAlgorithm,
            self.TokenWithInvalidAlgorithm,
            self.TokenWithoutIssuer,
            self.TokenWithInvalidIssuer,
            self.TokenWithoutIat,
            self.TokenWithInvalidIat,
            self.TokenWithIatInFuture,
            self.TokenWithoutNbf,
            self.TokenWithInvalidNbf,
            self.TokenWithNbfInFuture,
            self.TokenWithoutExp,
            self.TokenWithInvalidExp,
            self.TokenWithExpInPast,
            self.TokenSignedWithDifferentKey,
            self.InvalidSignedWithDifferentKeyForceArm,
            self.ValidToken
        ]
